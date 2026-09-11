"""Authenticated HTTP control plane and durable job worker."""

from __future__ import annotations

import hmac
import json
import os
import signal
import threading
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .conference import ConferenceEngine
from .config import load_yaml
from .diagnosis import DiagnosticEngine, seeded_excess_current_session, simulated_excess_current_observer
from .directory import AgentDirectory
from .evidence import EvidenceStore
from .jobs import JobQueue, JobWorker, job_as_dict
from .model_router import ModelRoutingPolicy
from .models import TaskManifest
from .project import ProjectIngestor
from .provider import DryRunProvider, HttpJsonProvider
from .report import write_report
from .routing import RoutingPolicy
from .storage import ConferenceStore


class ControlPlane:
    ALLOWED_OPERATIONS = {"conference", "project_ingest", "debug_demo", "evidence_text"}

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
        task_value = payload.get("task", payload)
        if not isinstance(task_value, dict):
            raise ValueError("conference payload requires a task object")
        task = TaskManifest.from_dict(task_value)
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
        rounds = int(payload.get("iterate_rounds", 0)) if "task" in payload else 0
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
            "state_path": str(self.data_root / "runs" / record.conference_id / "state.json"),
            "report_path": str(report),
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

    def __init__(self, address, control: ControlPlane, queue: JobQueue, api_token: str):
        super().__init__(address, CopilotRequestHandler)
        self.control = control
        self.queue = queue
        self.api_token = api_token


class CopilotRequestHandler(BaseHTTPRequestHandler):
    server: CopilotHttpServer
    protocol_version = "HTTP/1.1"
    max_body_bytes = 2_000_000

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health":
            self._json(HTTPStatus.OK, {
                "status": "ok",
                "agents": len(self.server.control.directory),
                "provider": self.server.control.provider_name,
            })
            return
        if not self._authorized():
            return
        if path.startswith("/v1/jobs/"):
            job_id = path.removeprefix("/v1/jobs/")
            try:
                self._json(HTTPStatus.OK, job_as_dict(self.server.queue.get(job_id)))
            except KeyError as exc:
                self._json(HTTPStatus.NOT_FOUND, {"error": str(exc)})
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
) -> None:
    if not api_token:
        raise ValueError("COPILOT_API_TOKEN is required")
    control = ControlPlane(
        repo_root, data_root, projects_root, provider_name,
        model_gateway_url, model_gateway_key,
    )
    queue = JobQueue(Path(data_root) / "jobs.sqlite3")
    worker = JobWorker(queue, control.execute)
    server = CopilotHttpServer((host, port), control, queue, api_token)
    stop_once = threading.Event()

    def stop_server(*_args) -> None:
        if stop_once.is_set():
            return
        stop_once.set()
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, stop_server)
    signal.signal(signal.SIGINT, stop_server)
    worker.start()
    try:
        server.serve_forever(poll_interval=0.25)
    finally:
        worker.stop()
        server.server_close()


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
