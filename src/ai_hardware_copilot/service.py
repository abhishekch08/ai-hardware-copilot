"""Authenticated HTTP control plane and durable job worker."""

from __future__ import annotations

import hmac
import json
import os
import re
import signal
import threading
from collections import Counter
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

from .conference import ConferenceEngine
from .config import load_yaml
from .diagnosis import DiagnosticEngine, seeded_excess_current_session, simulated_excess_current_observer
from .directory import AgentDirectory
from .evidence import EvidenceStore
from .idea import task_from_idea
from .jobs import JobQueue, JobWorker, job_as_dict, job_summary
from .model_router import ModelRoutingPolicy
from .models import TaskManifest
from .project import ProjectIngestor
from .provider import DryRunProvider, HttpJsonProvider
from .report import write_report
from .routing import RoutingPolicy
from .storage import ConferenceStore


class ControlPlane:
    ALLOWED_OPERATIONS = {
        "conference", "idea_conference", "project_ingest", "debug_demo", "evidence_text"
    }

    def __init__(
        self,
        repo_root: str | Path,
        data_root: str | Path,
        projects_root: str | Path,
        provider_name: str = "dry-run",
        model_gateway_url: str | None = None,
        model_gateway_key: str | None = None,
    ):
        self.repo_root = Path(repo_root).resolve()
        self.data_root = Path(data_root).resolve()
        self.projects_root = Path(projects_root).resolve()
        self.provider_name = provider_name
        self.model_gateway_url = model_gateway_url
        self.model_gateway_key = model_gateway_key
        self.evidence = EvidenceStore(self.data_root / "evidence")
        self.directory = AgentDirectory.from_directory(self.repo_root / "config" / "agents")
        self.routing = RoutingPolicy(
            self.directory,
            load_yaml(self.repo_root / "config" / "mandatory_review_rules.yaml"),
            load_yaml(self.repo_root / "config" / "capability_graph.yaml"),
        )
        self.model_policy = ModelRoutingPolicy(
            load_yaml(self.repo_root / "config" / "model_profiles.yaml")
        )

    def execute(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        if operation not in self.ALLOWED_OPERATIONS:
            raise ValueError(f"unsupported operation: {operation}")
        if operation == "evidence_text":
            record = self.evidence.register_bytes(
                str(payload["text"]).encode("utf-8"),
                kind=str(payload.get("kind", "text")),
                source_uri=str(payload.get("source_uri", "api://submitted-text")),
                media_type="text/plain",
                configuration=dict(payload.get("configuration", {})),
                metadata=dict(payload.get("metadata", {})),
            )
            return asdict(record)
        if operation == "project_ingest":
            relative_root = Path(str(payload.get("project_root", ".")))
            project_root = (self.projects_root / relative_root).resolve()
            _require_within(self.projects_root, project_root)
            manifest = payload.get("manifest")
            if not isinstance(manifest, dict):
                raise ValueError("project_ingest payload requires manifest object")
            index = ProjectIngestor(self.evidence).ingest(manifest, project_root)
            destination = (
                self.data_root / "projects" / index.project_id / index.hardware_revision / "index.json"
            )
            _write_json(destination, index.as_dict())
            return {"index": index.as_dict(), "path": str(destination)}
        if operation == "debug_demo":
            true_hypothesis = str(payload.get("true_hypothesis", "H_FW"))
            session = seeded_excess_current_session(str(payload.get("session_id", "seeded-current-001")))
            result = DiagnosticEngine(self.evidence).run(
                session,
                simulated_excess_current_observer(true_hypothesis),
                confidence_threshold=float(payload.get("confidence_threshold", 0.9)),
                max_steps=int(payload.get("max_steps", 3)),
            )
            return asdict(result)
        if operation == "idea_conference":
            task = task_from_idea(payload)
            return self._run_conference(task, _integer_rounds(payload.get("iterate_rounds", 3)))
        task_value = payload.get("task", payload)
        if not isinstance(task_value, dict):
            raise ValueError("conference payload requires a task object")
        task = TaskManifest.from_dict(task_value)
        rounds = _integer_rounds(payload.get("iterate_rounds", 0)) if "task" in payload else 0
        return self._run_conference(task, rounds)

    def _run_conference(self, task: TaskManifest, rounds: int) -> dict[str, Any]:
        if isinstance(rounds, bool) or not 0 <= rounds <= 10:
            raise ValueError("iterate_rounds must be from 0 through 10")
        unknown_agents = set(task.required_agents) - self.directory.ids
        if unknown_agents:
            raise ValueError(f"task requires unknown agents: {sorted(unknown_agents)}")
        if int(task.risk_tier[1:]) >= 3:
            invalid = [reference for reference in task.evidence_refs if not self.evidence.verify(reference)]
            if not task.evidence_refs or invalid:
                raise ValueError(
                    "T3/T4 service conferences require verified content-addressed evidence; "
                    f"invalid={invalid}"
                )
        provider = self._provider()
        store = ConferenceStore(self.data_root / "runs")
        engine = ConferenceEngine(self.directory, self.routing, provider, store, max_workers=8)
        record = engine.run_initial(task)
        if rounds:
            engine.iterate(record, max_rounds=rounds)
        report = self.data_root / "runs" / record.conference_id / "report.md"
        write_report(record, report)
        return {
            "conference_id": record.conference_id,
            "state": record.state.value,
            "proposal_version": record.task.proposal_version,
            "agents_screened": len(record.attendance),
            "active_agents": len(record.active_agents),
            "coverage_passed": bool(record.coverage_report and record.coverage_report.passed),
            "provider": self.provider_name,
            "state_path": str(self.data_root / "runs" / record.conference_id / "state.json"),
            "report_path": str(report),
        }

    def configuration(self) -> dict[str, Any]:
        reasoning_enabled = self.provider_name == "http" and bool(self.model_gateway_url)
        return {
            "product": "AI Hardware Engineer / Lab Copilot",
            "agents": len(self.directory),
            "provider": self.provider_name,
            "reasoning_enabled": reasoning_enabled,
            "mode_notice": (
                "Live specialist reasoning is configured. Engineering conclusions still require evidence."
                if reasoning_enabled else
                "Dry-run mode validates routing and safety gates; it does not perform specialist reasoning."
            ),
            "max_deliberation_rounds": 10,
            "supported_risk_tiers": ["T1", "T2", "T3", "T4"],
        }

    def conference_view(self, conference_id: str) -> dict[str, Any]:
        if re.fullmatch(r"CONF-[A-Za-z0-9][A-Za-z0-9._-]{0,95}", conference_id) is None:
            raise ValueError("invalid conference ID")
        record = ConferenceStore(self.data_root / "runs").load(conference_id)
        value = record.as_dict()
        version = record.task.proposal_version
        current_positions = [
            item for item in value["positions"] if item["proposal_version"] == version
        ]
        current_objections = [
            item for item in value["objections"] if item["proposal_version"] == version
        ]
        for item in current_positions:
            item["agent_name"] = self.directory.get(item["agent_id"]).name
        for item in current_objections:
            item["agent_name"] = self.directory.get(item["agent_id"]).name
        active_agents = [
            {
                "agent_id": agent_id,
                "agent_name": self.directory.get(agent_id).name,
                "relevance": value["attendance"][agent_id]["relevance"],
                "mandatory": value["attendance"][agent_id]["mandatory"],
            }
            for agent_id in record.active_agents
        ]
        report_path = self.data_root / "runs" / conference_id / "report.md"
        return {
            "conference_id": conference_id,
            "state": record.state.value,
            "provider": self.provider_name,
            "task": value["task"],
            "proposal_version": version,
            "current_round": record.current_round,
            "agents_screened": len(record.attendance),
            "active_agents": active_agents,
            "attendance_counts": dict(sorted(Counter(
                item.relevance.value for item in record.attendance.values()
            ).items())),
            "verdict_counts": dict(sorted(Counter(
                item["verdict"] for item in current_positions
            ).items())),
            "positions": current_positions,
            "objections": current_objections,
            "coverage_report": value["coverage_report"],
            "final_decision": value["final_decision"],
            "events": value["events"],
            "report_markdown": report_path.read_text(encoding="utf-8") if report_path.exists() else "",
        }

    def _provider(self):
        if self.provider_name == "dry-run":
            return DryRunProvider()
        if self.provider_name != "http":
            raise ValueError(f"unsupported reasoning provider: {self.provider_name}")
        if not self.model_gateway_url:
            raise ValueError("HTTP provider requires a model gateway URL")
        return HttpJsonProvider(
            endpoint=self.model_gateway_url,
            api_key=self.model_gateway_key,
            repo_root=self.repo_root,
            model_policy=self.model_policy,
        )


class CopilotHttpServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self, address, control: ControlPlane, queue: JobQueue, api_token: str,
        web_root: str | Path | None = None,
    ):
        super().__init__(address, CopilotRequestHandler)
        self.control = control
        self.queue = queue
        self.api_token = api_token
        self.web_root = Path(web_root or control.repo_root / "web").resolve()


class CopilotRequestHandler(BaseHTTPRequestHandler):
    server: CopilotHttpServer
    protocol_version = "HTTP/1.1"
    max_body_bytes = 2_000_000

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        if path in {"/", "/index.html", "/styles.css", "/app.js", "/favicon.svg", "/favicon.ico"}:
            self._static(path)
            return
        if path == "/health":
            self._json(HTTPStatus.OK, {
                "status": "ok",
                "agents": len(self.server.control.directory),
                "provider": self.server.control.provider_name,
            })
            return
        if not self._authorized():
            return
        if path == "/v1/config":
            self._json(HTTPStatus.OK, self.server.control.configuration())
            return
        if path == "/v1/jobs":
            try:
                query = parse_qs(parsed.query)
                limit = int(query.get("limit", ["50"])[0])
                self._json(HTTPStatus.OK, {
                    "jobs": [job_summary(job) for job in self.server.queue.list_recent(limit)]
                })
            except ValueError as exc:
                self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        if path.startswith("/v1/jobs/"):
            job_id = path.removeprefix("/v1/jobs/")
            try:
                self._json(HTTPStatus.OK, job_as_dict(self.server.queue.get(job_id)))
            except KeyError as exc:
                self._json(HTTPStatus.NOT_FOUND, {"error": str(exc)})
            return
        if path.startswith("/v1/conferences/"):
            conference_id = path.removeprefix("/v1/conferences/")
            try:
                self._json(HTTPStatus.OK, self.server.control.conference_view(conference_id))
            except FileNotFoundError:
                self._json(HTTPStatus.NOT_FOUND, {"error": "conference not found"})
            except ValueError as exc:
                self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if not self._authorized():
            return
        path = urlparse(self.path).path
        if path != "/v1/jobs":
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        try:
            body = self._read_json()
            operation = str(body.get("operation", ""))
            payload = body.get("payload", {})
            if operation not in self.server.control.ALLOWED_OPERATIONS:
                raise ValueError(f"unsupported operation: {operation}")
            if not isinstance(payload, dict):
                raise ValueError("payload must be an object")
            idempotency_key = self.headers.get("Idempotency-Key")
            job = self.server.queue.enqueue(operation, payload, idempotency_key)
            self._json(HTTPStatus.ACCEPTED, job_as_dict(job))
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})

    def _authorized(self) -> bool:
        supplied = self.headers.get("Authorization", "")
        expected = f"Bearer {self.server.api_token}"
        if not self.server.api_token or not hmac.compare_digest(supplied, expected):
            self._json(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
            return False
        return True

    def _read_json(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("invalid Content-Length") from exc
        if length <= 0 or length > self.max_body_bytes:
            raise ValueError("request body size is invalid")
        value = json.loads(self.rfile.read(length))
        if not isinstance(value, dict):
            raise ValueError("request body must be a JSON object")
        return value

    def _json(self, status: HTTPStatus, value: dict[str, Any]) -> None:
        data = (json.dumps(value, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(data)

    def _static(self, request_path: str) -> None:
        names = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/index.html": ("index.html", "text/html; charset=utf-8"),
            "/styles.css": ("styles.css", "text/css; charset=utf-8"),
            "/app.js": ("app.js", "text/javascript; charset=utf-8"),
            "/favicon.svg": ("favicon.svg", "image/svg+xml"),
            "/favicon.ico": ("favicon.svg", "image/svg+xml"),
        }
        filename, media_type = names[request_path]
        source = (self.server.web_root / filename).resolve()
        try:
            source.relative_to(self.server.web_root)
            data = source.read_bytes()
        except (ValueError, FileNotFoundError):
            self._json(HTTPStatus.NOT_FOUND, {"error": "web interface is unavailable"})
            return
        self.send_response(HTTPStatus.OK.value)
        self.send_header("Content-Type", media_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
            "base-uri 'none'; form-action 'self'; frame-ancestors 'none'",
        )
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args) -> None:
        return


def serve(
    *,
    repo_root: str | Path,
    data_root: str | Path,
    projects_root: str | Path,
    host: str,
    port: int,
    api_token: str,
    provider_name: str = "dry-run",
    model_gateway_url: str | None = None,
    model_gateway_key: str | None = None,
    on_ready: Callable[[], None] | None = None,
) -> None:
    if not api_token:
        raise ValueError("COPILOT_API_TOKEN is required")
    control = ControlPlane(
        repo_root, data_root, projects_root, provider_name,
        model_gateway_url, model_gateway_key,
    )
    queue = JobQueue(Path(data_root) / "jobs.sqlite3")
    worker = JobWorker(queue, control.execute)
    server = CopilotHttpServer(
        (host, port), control, queue, api_token, Path(repo_root) / "web"
    )
    stop_once = threading.Event()

    def stop_server(*_args) -> None:
        if stop_once.is_set():
            return
        stop_once.set()
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, stop_server)
    signal.signal(signal.SIGINT, stop_server)
    worker.start()
    if on_ready:
        on_ready()
    try:
        server.serve_forever(poll_interval=0.25)
    finally:
        worker.stop()
        server.server_close()


def _integer_rounds(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("iterate_rounds must be an integer from 0 through 10")
    if isinstance(value, str) and not re.fullmatch(r"\d+", value.strip()):
        raise ValueError("iterate_rounds must be an integer from 0 through 10")
    if isinstance(value, float) and not value.is_integer():
        raise ValueError("iterate_rounds must be an integer from 0 through 10")
    try:
        rounds = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("iterate_rounds must be an integer from 0 through 10") from exc
    if not 0 <= rounds <= 10:
        raise ValueError("iterate_rounds must be an integer from 0 through 10")
    return rounds


def _require_within(root: Path, path: Path) -> None:
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes configured projects root: {path}") from exc


def _write_json(destination: Path, value: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, destination)
