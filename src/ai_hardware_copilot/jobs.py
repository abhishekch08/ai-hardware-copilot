"""Small durable SQLite job queue for the single-node/on-prem MVP."""

from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


@dataclass(slots=True)
class Job:
    job_id: str
    operation: str
    status: str
    payload: dict[str, Any]
    result: dict[str, Any] | None
    error: str | None
    created_at: str
    updated_at: str
    idempotency_key: str | None


class JobQueue:
    def __init__(self, database: str | Path):
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=30, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def _initialize(self) -> None:
        with closing(self._connect()) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    operation TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('queued','running','succeeded','failed')),
                    payload_json TEXT NOT NULL,
                    result_json TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    idempotency_key TEXT UNIQUE
                )
            """)
            connection.execute(
                "UPDATE jobs SET status='queued', updated_at=? WHERE status='running'",
                (_now(),),
            )

    def enqueue(
        self,
        operation: str,
        payload: dict[str, Any],
        idempotency_key: str | None = None,
    ) -> Job:
        if not operation.strip():
            raise ValueError("operation cannot be empty")
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        timestamp = _now()
        job_id = f"JOB-{uuid.uuid4().hex}"
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            if idempotency_key:
                existing = connection.execute(
                    "SELECT * FROM jobs WHERE idempotency_key=?", (idempotency_key,)
                ).fetchone()
                if existing:
                    if existing["operation"] != operation or existing["payload_json"] != canonical:
                        connection.execute("ROLLBACK")
                        raise ValueError(
                            "idempotency key was already used with a different operation or payload"
                        )
                    connection.execute("COMMIT")
                    return _row_to_job(existing)
            connection.execute(
                """INSERT INTO jobs
                   (job_id, operation, status, payload_json, created_at, updated_at, idempotency_key)
                   VALUES (?, ?, 'queued', ?, ?, ?, ?)""",
                (job_id, operation, canonical, timestamp, timestamp, idempotency_key),
            )
            row = connection.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
            connection.execute("COMMIT")
        return _row_to_job(row)

    def claim_next(self) -> Job | None:
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM jobs WHERE status='queued' ORDER BY created_at, job_id LIMIT 1"
            ).fetchone()
            if row is None:
                connection.execute("COMMIT")
                return None
            timestamp = _now()
            connection.execute(
                "UPDATE jobs SET status='running', updated_at=? WHERE job_id=? AND status='queued'",
                (timestamp, row["job_id"]),
            )
            updated = connection.execute(
                "SELECT * FROM jobs WHERE job_id=?", (row["job_id"],)
            ).fetchone()
            connection.execute("COMMIT")
        return _row_to_job(updated)

    def complete(self, job_id: str, result: dict[str, Any]) -> Job:
        canonical = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        with closing(self._connect()) as connection:
            cursor = connection.execute(
                """UPDATE jobs SET status='succeeded', result_json=?, error=NULL, updated_at=?
                   WHERE job_id=? AND status='running'""",
                (canonical, _now(), job_id),
            )
            if cursor.rowcount != 1:
                raise ValueError(f"job cannot be completed from its current state: {job_id}")
        return self.get(job_id)

    def fail(self, job_id: str, error: str) -> Job:
        with closing(self._connect()) as connection:
            cursor = connection.execute(
                """UPDATE jobs SET status='failed', error=?, updated_at=?
                   WHERE job_id=? AND status='running'""",
                (error[:4000], _now(), job_id),
            )
            if cursor.rowcount != 1:
                raise ValueError(f"job cannot be failed from its current state: {job_id}")
        return self.get(job_id)

    def get(self, job_id: str) -> Job:
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(f"unknown job: {job_id}")
        return _row_to_job(row)


class JobWorker:
    def __init__(self, queue: JobQueue, handler: Callable[[str, dict[str, Any]], dict[str, Any]]):
        self.queue = queue
        self.handler = handler
        self.stop_event = threading.Event()
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        if self.thread and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self.run, name="copilot-job-worker", daemon=True)
        self.thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=timeout)

    def run(self) -> None:
        while not self.stop_event.is_set():
            job = self.queue.claim_next()
            if job is None:
                self.stop_event.wait(0.25)
                continue
            try:
                self.queue.complete(job.job_id, self.handler(job.operation, job.payload))
            except Exception as exc:  # the persisted error is the job boundary
                self.queue.fail(job.job_id, f"{type(exc).__name__}: {exc}")


def job_as_dict(job: Job) -> dict[str, Any]:
    return {
        "job_id": job.job_id,
        "operation": job.operation,
        "status": job.status,
        "payload": job.payload,
        "result": job.result,
        "error": job.error,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "idempotency_key": job.idempotency_key,
    }


def _row_to_job(row: sqlite3.Row) -> Job:
    return Job(
        job_id=row["job_id"],
        operation=row["operation"],
        status=row["status"],
        payload=json.loads(row["payload_json"]),
        result=json.loads(row["result_json"]) if row["result_json"] else None,
        error=row["error"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        idempotency_key=row["idempotency_key"],
    )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
