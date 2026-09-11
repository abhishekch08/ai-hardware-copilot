"""Command-line entry point for compilation and conference execution."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import yaml

from .conference import ConferenceEngine
from .config import load_yaml
from .directory import AgentDirectory
from .models import TaskManifest
from .provider import DryRunProvider, HttpJsonProvider
from .report import write_report
from .routing import RoutingPolicy
from .storage import ConferenceStore


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_mapping(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    with source.open("r", encoding="utf-8") as handle:
        if source.suffix.lower() == ".json":
            value = json.load(handle)
        else:
            value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{source} must contain a mapping")
    return value


def build_runtime(args):
    root = Path(args.repo_root).resolve()
    directory = AgentDirectory.from_directory(root / "config" / "agents")
    routing = RoutingPolicy(
        directory,
        load_yaml(root / "config" / "mandatory_review_rules.yaml"),
        load_yaml(root / "config" / "capability_graph.yaml"),
    )
    if args.provider == "dry-run":
        provider = DryRunProvider()
    else:
        endpoint = args.endpoint or os.environ.get("COPILOT_MODEL_GATEWAY_URL")
        if not endpoint:
            raise ValueError("HTTP provider requires --endpoint or COPILOT_MODEL_GATEWAY_URL")
        key = os.environ.get(args.api_key_env) if args.api_key_env else None
        provider = HttpJsonProvider(
            endpoint=endpoint,
            api_key=key,
            timeout_s=args.timeout,
            repo_root=root,
        )
    store = ConferenceStore(Path(args.output_root))
    engine = ConferenceEngine(directory, routing, provider, store, max_workers=args.max_workers)
    return root, directory, routing, engine, store


def add_runtime_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo-root", default=str(repo_root()))
    parser.add_argument("--output-root", default="runs")
    parser.add_argument("--provider", choices=("dry-run", "http"), default="dry-run")
    parser.add_argument("--endpoint")
    parser.add_argument("--api-key-env", default="COPILOT_MODEL_GATEWAY_API_KEY")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--max-workers", type=int, default=8)


def command_validate(args) -> int:
    _, directory, routing, _, _ = build_runtime(args)
    if len(directory) != 184:
        raise ValueError(f"expected 184 compiled agents, found {len(directory)}")
    print(json.dumps({
        "status": "valid",
        "agents": len(directory),
        "review_rules": len(routing.rules),
    }, indent=2))
    return 0


def command_run(args) -> int:
    _, _, _, engine, _ = build_runtime(args)
    task = TaskManifest.from_dict(read_mapping(args.task))
    record = engine.run_initial(task)
    if args.iterate_rounds:
        engine.iterate(record, max_rounds=args.iterate_rounds)
    path = Path(args.output_root) / record.conference_id / "report.md"
    write_report(record, path)
    print(json.dumps({
        "conference_id": record.conference_id,
        "state": record.state.value,
        "agents_screened": len(record.attendance),
        "active_agents": len(record.active_agents),
        "current_objections": sum(
            item.proposal_version == record.task.proposal_version and item.status != "resolved"
            for item in record.objections
        ),
        "coverage_passed": bool(record.coverage_report and record.coverage_report.passed),
        "record": str(Path(args.output_root) / record.conference_id / "state.json"),
        "report": str(path),
    }, indent=2))
    return 0


def command_status(args) -> int:
    _, _, _, _, store = build_runtime(args)
    record = store.load(args.conference_id)
    path = Path(args.output_root) / record.conference_id / "report.md"
    write_report(record, path)
    print(json.dumps({
        "conference_id": record.conference_id,
        "state": record.state.value,
        "proposal_version": record.task.proposal_version,
        "active_agents": len(record.active_agents),
        "open_objections": [
            item.objection_id for item in record.objections
            if item.proposal_version == record.task.proposal_version and item.status != "resolved"
        ],
        "report": str(path),
    }, indent=2))
    return 0


def command_revise(args) -> int:
    _, _, _, engine, store = build_runtime(args)
    record = store.load(args.conference_id)
    revision = read_mapping(args.revision)
    engine.revise_proposal(
        record,
        changes=revision.get("changes", {}),
        changed_interfaces=list(revision.get("changed_interfaces", [])),
        evidence_refs=list(revision.get("evidence_refs", [])),
        actor=str(revision.get("actor", "META-03")),
    )
    engine.collect_independent_positions(record)
    engine.coverage(record)
    store.save(record)
    path = Path(args.output_root) / record.conference_id / "report.md"
    write_report(record, path)
    print(json.dumps({
        "conference_id": record.conference_id,
        "proposal_version": record.task.proposal_version,
        "state": record.state.value,
        "agents_rescreened": len(record.attendance),
        "active_agents": len(record.active_agents),
        "report": str(path),
    }, indent=2))
    return 0


def command_resolve(args) -> int:
    _, _, _, engine, store = build_runtime(args)
    record = store.load(args.conference_id)
    engine.resolve_objection(
        record,
        objection_id=args.objection_id,
        resolution=args.resolution,
        resolved_by=args.resolved_by,
        evidence_refs=args.evidence_ref,
    )
    engine.coverage(record)
    store.save(record)
    write_report(record, Path(args.output_root) / record.conference_id / "report.md")
    print(json.dumps({"objection_id": args.objection_id, "status": "resolved"}, indent=2))
    return 0


def command_iterate(args) -> int:
    _, _, _, engine, store = build_runtime(args)
    record = store.load(args.conference_id)
    engine.iterate(record, max_rounds=args.max_rounds)
    store.save(record)
    path = Path(args.output_root) / record.conference_id / "report.md"
    write_report(record, path)
    print(json.dumps({
        "conference_id": record.conference_id,
        "state": record.state.value,
        "proposal_version": record.task.proposal_version,
        "rounds_completed": record.current_round,
        "open_objections": sum(
            item.proposal_version == record.task.proposal_version and item.status != "resolved"
            for item in record.objections
        ),
        "report": str(path),
    }, indent=2))
    return 0


def command_finalize(args) -> int:
    _, _, _, engine, store = build_runtime(args)
    record = store.load(args.conference_id)
    report = engine.finalize(record, args.summary, args.accepted_risk)
    write_report(record, Path(args.output_root) / record.conference_id / "report.md")
    print(json.dumps({
        "conference_id": record.conference_id,
        "state": record.state.value,
        "coverage_passed": report.passed,
        "failures": report.failures,
    }, indent=2))
    return 0 if report.passed else 2


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="hardware-copilot")
    commands = root.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    add_runtime_arguments(validate)
    validate.set_defaults(handler=command_validate)
    run = commands.add_parser("run")
    add_runtime_arguments(run)
    run.add_argument("--task", required=True)
    run.add_argument("--iterate-rounds", type=int, default=0)
    run.set_defaults(handler=command_run)
    status = commands.add_parser("status")
    add_runtime_arguments(status)
    status.add_argument("conference_id")
    status.set_defaults(handler=command_status)
    revise = commands.add_parser("revise")
    add_runtime_arguments(revise)
    revise.add_argument("conference_id")
    revise.add_argument("--revision", required=True)
    revise.set_defaults(handler=command_revise)
    resolve = commands.add_parser("resolve")
    add_runtime_arguments(resolve)
    resolve.add_argument("conference_id")
    resolve.add_argument("objection_id")
    resolve.add_argument("--resolution", required=True)
    resolve.add_argument("--resolved-by", required=True)
    resolve.add_argument("--evidence-ref", action="append", default=[])
    resolve.set_defaults(handler=command_resolve)
    iterate = commands.add_parser("iterate")
    add_runtime_arguments(iterate)
    iterate.add_argument("conference_id")
    iterate.add_argument("--max-rounds", type=int, default=3)
    iterate.set_defaults(handler=command_iterate)
    finalize = commands.add_parser("finalize")
    add_runtime_arguments(finalize)
    finalize.add_argument("conference_id")
    finalize.add_argument("--summary", required=True)
    finalize.add_argument("--accepted-risk", action="append", default=[])
    finalize.set_defaults(handler=command_finalize)
    return root


def main() -> None:
    args = parser().parse_args()
    raise SystemExit(args.handler(args))


if __name__ == "__main__":
    main()
