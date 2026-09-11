"""Content-addressed evidence and provenance storage.

The store proves which bytes and configuration a reference denotes. It deliberately does
not claim that a document semantically supports a conclusion; that remains a critic/tool
responsibility recorded through claim assessments.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class EvidenceRecord:
    evidence_id: str
    sha256: str
    kind: str
    source_uri: str
    media_type: str
    byte_count: int
    created_at: str
    configuration: dict[str, Any] = field(default_factory=dict)
    derived_from: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "EvidenceRecord":
        return cls(**value)


@dataclass(slots=True)
class ClaimAssessment:
    claim_id: str
    claim: str
    status: str
    evidence_refs: list[str]
    method: str
    assessor: str
    assessed_at: str
    notes: str = ""


class EvidenceStore:
    """Immutable blobs plus atomic metadata records and claim assessments."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.blobs = self.root / "blobs"
        self.records = self.root / "records"
        self.claims = self.root / "claims"

    def register_file(
        self,
        source: str | Path,
        *,
        kind: str,
        configuration: dict[str, Any] | None = None,
        derived_from: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EvidenceRecord:
        path = Path(source).resolve()
        data = path.read_bytes()
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        return self.register_bytes(
            data,
            kind=kind,
            source_uri=path.as_uri(),
            media_type=media_type,
            configuration=configuration,
            derived_from=derived_from,
            metadata={"filename": path.name, **(metadata or {})},
        )

    def register_json(
        self,
        value: Any,
        *,
        kind: str,
        source_uri: str,
        configuration: dict[str, Any] | None = None,
        derived_from: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EvidenceRecord:
        data = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return self.register_bytes(
            data,
            kind=kind,
            source_uri=source_uri,
            media_type="application/json",
            configuration=configuration,
            derived_from=derived_from,
            metadata=metadata,
        )

    def register_bytes(
        self,
        data: bytes,
        *,
        kind: str,
        source_uri: str,
        media_type: str = "application/octet-stream",
        configuration: dict[str, Any] | None = None,
        derived_from: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EvidenceRecord:
        digest = hashlib.sha256(data).hexdigest()
        parents = sorted(set(derived_from or []))
        for parent in parents:
            if not self.verify(parent):
                raise ValueError(f"derived evidence parent is missing or corrupt: {parent}")
        identity = _record_identity(
            sha256=digest,
            kind=kind,
            source_uri=source_uri,
            media_type=media_type,
            byte_count=len(data),
            configuration=configuration or {},
            derived_from=parents,
            metadata=metadata or {},
        )
        record_digest = hashlib.sha256(
            json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        evidence_id = f"evidence://sha256/{record_digest}"
        record_path = self.records / f"{record_digest}.json"
        if record_path.exists():
            if not self.verify(evidence_id):
                raise ValueError(f"existing evidence record is corrupt: {evidence_id}")
            return EvidenceRecord.from_dict(json.loads(record_path.read_text(encoding="utf-8")))
        record = EvidenceRecord(
            evidence_id=evidence_id,
            sha256=digest,
            kind=kind,
            source_uri=source_uri,
            media_type=media_type,
            byte_count=len(data),
            created_at=_now(),
            configuration=configuration or {},
            derived_from=parents,
            metadata=metadata or {},
        )
        self._write_once(self.blobs / digest, data)
        self._write_once(
            record_path,
            (json.dumps(asdict(record), indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
        return record

    def get(self, evidence_ref: str) -> EvidenceRecord:
        record_digest = _digest_from_ref(evidence_ref)
        source = self.records / f"{record_digest}.json"
        value = json.loads(source.read_text(encoding="utf-8"))
        return EvidenceRecord.from_dict(value)

    def read_bytes(self, evidence_ref: str) -> bytes:
        record = self.get(evidence_ref)
        data = (self.blobs / record.sha256).read_bytes()
        if hashlib.sha256(data).hexdigest() != record.sha256:
            raise ValueError(f"evidence blob hash mismatch: {evidence_ref}")
        return data

    def verify(self, evidence_ref: str) -> bool:
        try:
            record = self.get(evidence_ref)
            if record.evidence_id != evidence_ref:
                return False
            expected_record_digest = hashlib.sha256(
                json.dumps(
                    _record_identity(
                        sha256=record.sha256,
                        kind=record.kind,
                        source_uri=record.source_uri,
                        media_type=record.media_type,
                        byte_count=record.byte_count,
                        configuration=record.configuration,
                        derived_from=record.derived_from,
                        metadata=record.metadata,
                    ),
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                ).encode("utf-8")
            ).hexdigest()
            if expected_record_digest != _digest_from_ref(evidence_ref):
                return False
            if record.byte_count != (self.blobs / record.sha256).stat().st_size:
                return False
            return hashlib.sha256((self.blobs / record.sha256).read_bytes()).hexdigest() == record.sha256
        except (FileNotFoundError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            return False

    def assess_claim(
        self,
        *,
        claim_id: str,
        claim: str,
        status: str,
        evidence_refs: list[str],
        method: str,
        assessor: str,
        notes: str = "",
    ) -> ClaimAssessment:
        if status not in {"supported", "contradicted", "inconclusive"}:
            raise ValueError("claim status must be supported, contradicted or inconclusive")
        if status != "inconclusive" and not evidence_refs:
            raise ValueError("supported/contradicted claims require evidence")
        invalid = [ref for ref in evidence_refs if not self.verify(ref)]
        if invalid:
            raise ValueError(f"claim references invalid evidence: {invalid}")
        assessment = ClaimAssessment(
            claim_id=claim_id,
            claim=claim,
            status=status,
            evidence_refs=sorted(set(evidence_refs)),
            method=method,
            assessor=assessor,
            assessed_at=_now(),
            notes=notes,
        )
        destination = self.claims / f"{claim_id}.json"
        self._atomic_replace(
            destination,
            (json.dumps(asdict(assessment), indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
        return assessment

    @staticmethod
    def _write_once(destination: Path, data: bytes) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if destination.read_bytes() != data:
                raise ValueError(f"immutable evidence collision at {destination}")
            return
        temporary = destination.with_name(
            f".{destination.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}"
        )
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError:
            if destination.read_bytes() != data:
                raise ValueError(f"immutable evidence collision at {destination}")
        finally:
            temporary.unlink(missing_ok=True)

    @staticmethod
    def _atomic_replace(destination: Path, data: bytes) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(
            f".{destination.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}"
        )
        with temporary.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)


def _digest_from_ref(evidence_ref: str) -> str:
    prefix = "evidence://sha256/"
    if not evidence_ref.startswith(prefix):
        raise ValueError(f"unsupported evidence reference: {evidence_ref}")
    digest = evidence_ref[len(prefix):]
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise ValueError(f"invalid evidence digest: {evidence_ref}")
    return digest


def _record_identity(
    *,
    sha256: str,
    kind: str,
    source_uri: str,
    media_type: str,
    byte_count: int,
    configuration: dict[str, Any],
    derived_from: list[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "blob_sha256": sha256,
        "kind": kind,
        "source_uri": source_uri,
        "media_type": media_type,
        "byte_count": byte_count,
        "configuration": configuration,
        "derived_from": sorted(set(derived_from)),
        "metadata": metadata,
    }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
