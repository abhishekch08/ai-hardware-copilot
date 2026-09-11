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
from .diagnosis import DiagnosticEngine, seeded_excess_current_session, simulated_excess_current_observer
from .directory import AgentDirectory
from .evidence import EvidenceStore
from .models import TaskManifest
from .model_router import ModelRoutingPolicy
from .project import ProjectIngestor
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
            model_policy=ModelRoutingPolicy(load_yaml(root / "config" / "model_profiles.yaml")),
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


def command_evidence_register(args) -> int:
    store = EvidenceStore(Path(args.data_root) / "evidence")
    record = store.register_file(
        args.file,
        kind=args.kind,
        configuration=read_mapping(args.configuration) if args.configuration else {},
        metadata={"submitted_by": args.submitted_by},
    )
    print(json.dumps(record.__dict__ if hasattr(record, "__dict__") else {
        field: getattr(record, field) for field in record.__dataclass_fields__
    }, indent=2))
    return 0


def command_evidence_verify(args) -> int:
    store = EvidenceStore(Path(args.data_root) / "evidence")
    verified = store.verify(args.evidence_ref)
    print(json.dumps({"evidence_ref": args.evidence_ref, "verified": verified}, indent=2))
    return 0 if verified else 2


def command_project_ingest(args) -> int:
    data_root = Path(args.data_root).resolve()
    manifest = read_mapping(args.manifest)
    index = ProjectIngestor(EvidenceStore(data_root / "evidence")).ingest(
        manifest, Path(args.project_root)
    )
    destination = data_root / "projects" / index.project_id / index.hardware_revision / "index.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(index.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, destination)
    print(json.dumps({
        "project_id": index.project_id,
        "hardware_revision": index.hardware_revision,
        "nodes": len(index.nodes),
        "edges": len(index.edges),
        "evidence_records": len(index.source_evidence),
        "warnings": index.warnings,
        "index": str(destination),
    }, indent=2))
    return 0


def command_debug_demo(args) -> int:
    data_root = Path(args.data_root).resolve()
    session = seeded_excess_current_session(args.session_id)
    result = DiagnosticEngine(EvidenceStore(data_root / "evidence")).run(
        session,
        simulated_excess_current_observer(args.true_hypothesis),
        confidence_threshold=args.confidence_threshold,
        max_steps=args.max_steps,
    )
    print(json.dumps({
        "session_id": result.session_id,
        "status": result.status,
        "steps": [
            {
                "experiment_id": step.experiment_id,
                "observed_outcome": step.observed_outcome,
                "information_gain_bits": round(step.expected_information_gain_bits, 6),
                "posterior": step.posterior,
                "evidence_ref": step.evidence_ref,
            }
            for step in result.steps
        ],
        "hypotheses": [
            {"id": item.hypothesis_id, "probability": item.probability, "status": item.status}
            for item in result.hypotheses
        ],
    }, indent=2))
    return 0 if result.status == "root_cause_candidate" else 2


def command_model_route(args) -> int:
    root = Path(args.repo_root).resolve()
    task = TaskManifest.from_dict(read_mapping(args.task))
    policy = ModelRoutingPolicy(load_yaml(root / "config" / "model_profiles.yaml"))
    route = policy.select(task, args.operation, active_agent_count=args.active_agents)
    print(json.dumps(route.as_dict(), indent=2))
    return 0


def command_serve(args) -> int:
    from .service import serve

    token = os.environ.get(args.api_token_env, "")
    gateway_key = os.environ.get(args.gateway_key_env, "") if args.gateway_key_env else None
    serve(
        repo_root=Path(args.repo_root).resolve(),
        data_root=Path(args.data_root).resolve(),
        projects_root=Path(args.projects_root).resolve(),
        host=args.host,
        port=args.port,
        api_token=token,
        provider_name=args.provider,
        model_gateway_url=args.endpoint or os.environ.get("COPILOT_MODEL_GATEWAY_URL"),
        model_gateway_key=gateway_key,
    )
    return 0


def command_gateway(args) -> int:
    from .gateway import models_from_environment, serve_gateway

    inbound_token = os.environ.get(args.api_token_env, "")
    backend_key = os.environ.get(args.backend_key_env, "")
    endpoint = args.backend_endpoint or os.environ.get("COPILOT_MODEL_BACKEND_URL", "")
    models = models_from_environment()
    serve_gateway(
        host=args.host,
        port=args.port,
        api_token=inbound_token,
        backend_endpoint=endpoint,
        backend_api_key=backend_key,
        models=models,
        timeout_s=args.timeout,
    )
    return 0


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
    evidence_register = commands.add_parser("evidence-register")
    evidence_register.add_argument("--data-root", default="data")
    evidence_register.add_argument("--file", required=True)
    evidence_register.add_argument("--kind", required=True)
    evidence_register.add_argument("--configuration")
    evidence_register.add_argument("--submitted-by", default="HUMAN-AUTHORITY")
    evidence_register.set_defaults(handler=command_evidence_register)
    evidence_verify = commands.add_parser("evidence-verify")
    evidence_verify.add_argument("--data-root", default="data")
    evidence_verify.add_argument("evidence_ref")
    evidence_verify.set_defaults(handler=command_evidence_verify)
    project_ingest = commands.add_parser("project-ingest")
    project_ingest.add_argument("--data-root", default="data")
    project_ingest.add_argument("--manifest", required=True)
    project_ingest.add_argument("--project-root", required=True)
    project_ingest.set_defaults(handler=command_project_ingest)
    debug_demo = commands.add_parser("debug-demo")
    debug_demo.add_argument("--data-root", default="data")
    debug_demo.add_argument("--session-id", default="seeded-current-001")
    debug_demo.add_argument("--true-hypothesis", choices=("H_LEAK", "H_FW", "H_REG"), default="H_FW")
    debug_demo.add_argument("--confidence-threshold", type=float, default=0.9)
    debug_demo.add_argument("--max-steps", type=int, default=3)
    debug_demo.set_defaults(handler=command_debug_demo)
    model_route = commands.add_parser("model-route")
    model_route.add_argument("--repo-root", default=str(repo_root()))
    model_route.add_argument("--task", required=True)
    model_route.add_argument("--operation", default="independent_analysis")
    model_route.add_argument("--active-agents", type=int, default=1)
    model_route.set_defaults(handler=command_model_route)
    service = commands.add_parser("serve")
    service.add_argument("--repo-root", default=str(repo_root()))
    service.add_argument("--data-root", default="data")
    service.add_argument("--projects-root", default="projects")
    service.add_argument("--host", default="127.0.0.1")
    service.add_argument("--port", type=int, default=8080)
    service.add_argument("--provider", choices=("dry-run", "http"), default="dry-run")
    service.add_argument("--endpoint")
    service.add_argument("--api-token-env", default="COPILOT_API_TOKEN")
    service.add_argument("--gateway-key-env", default="COPILOT_MODEL_GATEWAY_API_KEY")
    service.set_defaults(handler=command_serve)
    gateway = commands.add_parser("gateway")
    gateway.add_argument("--host", default="127.0.0.1")
    gateway.add_argument("--port", type=int, default=8090)
    gateway.add_argument("--api-token-env", default="COPILOT_MODEL_GATEWAY_API_KEY")
    gateway.add_argument("--backend-key-env", default="COPILOT_MODEL_BACKEND_API_KEY")
    gateway.add_argument("--backend-endpoint")
    gateway.add_argument("--timeout", type=float, default=180.0)
    gateway.set_defaults(handler=command_gateway)
    return root


def main() -> None:
    args = parser().parse_args()
    raise SystemExit(args.handler(args))


if __name__ == "__main__":
    main()
