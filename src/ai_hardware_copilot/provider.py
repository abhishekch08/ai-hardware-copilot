"""Replaceable reasoning-provider boundary.

Providers return auditable summaries, not hidden chain-of-thought. The included dry-run
provider is intentionally incapable of approving engineering work.
"""

from __future__ import annotations

import json
import hashlib
import math
import urllib.request
from dataclasses import asdict
from pathlib import Path
from typing import Any, Protocol

from .models import (
    AgentConfig,
    AgentPosition,
    AttendanceRecord,
    DeliberationContribution,
    SynthesisResult,
    TaskManifest,
    Verdict,
)


class ReasoningProvider(Protocol):
    name: str

    def assess_relevance(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        deterministic: AttendanceRecord,
    ) -> AttendanceRecord: ...

    def analyze(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        shared_context: dict[str, Any],
    ) -> AgentPosition: ...

    def deliberate(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        shared_context: dict[str, Any],
    ) -> DeliberationContribution: ...

    def synthesize(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        contributions: list[DeliberationContribution],
        shared_context: dict[str, Any],
    ) -> SynthesisResult: ...


class DryRunProvider:
    """Exercises routing/state/persistence without pretending to perform AI analysis."""

    name = "dry-run"

    def assess_relevance(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        deterministic: AttendanceRecord,
    ) -> AttendanceRecord:
        return deterministic

    def analyze(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        shared_context: dict[str, Any],
    ) -> AgentPosition:
        return AgentPosition(
            agent_id=agent.agent_id,
            proposal_version=task.proposal_version,
            verdict=Verdict.INSUFFICIENT_EVIDENCE,
            confidence=0.0,
            rationale="Dry-run mode validates orchestration only; no domain reasoning model was called.",
            risks=["A deterministic dry run cannot validate the engineering proposal."],
            conditions=["Run with a configured reasoning provider and authoritative project evidence."],
            verification=["Independent domain analysis and evidence review are required."],
        )

    def deliberate(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        shared_context: dict[str, Any],
    ) -> DeliberationContribution:
        return DeliberationContribution(
            agent_id=agent.agent_id,
            proposal_version=task.proposal_version,
            round_number=int(shared_context["round_number"]),
            rationale="Dry-run mode cannot resolve engineering objections.",
        )

    def synthesize(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        contributions: list[DeliberationContribution],
        shared_context: dict[str, Any],
    ) -> SynthesisResult:
        return SynthesisResult(
            proposal_version=task.proposal_version,
            round_number=int(shared_context["round_number"]),
            rationale="Dry-run mode cannot synthesize a technically justified revision.",
            unresolved_objection_ids=list(shared_context.get("open_objection_ids", [])),
        )


class ScriptedProvider:
    """Deterministic provider for evaluation and integration tests."""

    name = "scripted"

    def __init__(self, responses: dict[str, dict[str, Any]] | None = None):
        self.responses = responses or {}

    def assess_relevance(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        deterministic: AttendanceRecord,
    ) -> AttendanceRecord:
        return deterministic

    def analyze(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        shared_context: dict[str, Any],
    ) -> AgentPosition:
        value = self.responses.get(agent.agent_id, {})
        verdict = Verdict(value.get("verdict", Verdict.APPROVE.value))
        return AgentPosition(
            agent_id=agent.agent_id,
            proposal_version=task.proposal_version,
            verdict=verdict,
            confidence=float(value.get("confidence", 0.9)),
            rationale=value.get("rationale", "Scripted evaluation response."),
            claims=list(value.get("claims", [])),
            assumptions=list(value.get("assumptions", [])),
            risks=list(value.get("risks", [])),
            conditions=list(value.get("conditions", [])),
            evidence_refs=list(value.get("evidence_refs", task.evidence_refs)),
            requested_agents=list(value.get("requested_agents", [])),
            verification=list(value.get("verification", ["Scripted verification fixture."])),
        )

    def deliberate(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        shared_context: dict[str, Any],
    ) -> DeliberationContribution:
        value = self.responses.get(agent.agent_id, {}).get("deliberation", {})
        return DeliberationContribution(
            agent_id=agent.agent_id,
            proposal_version=task.proposal_version,
            round_number=int(shared_context["round_number"]),
            rationale=value.get("rationale", "Scripted deliberation fixture."),
            responses=list(value.get("responses", [])),
            counterarguments=list(value.get("counterarguments", [])),
            proposed_changes=dict(value.get("proposed_changes", {})),
            changed_interfaces=list(value.get("changed_interfaces", [])),
            evidence_refs=list(value.get("evidence_refs", [])),
            resolve_objection_ids=list(value.get("resolve_objection_ids", [])),
            requested_agents=list(value.get("requested_agents", [])),
        )

    def synthesize(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        contributions: list[DeliberationContribution],
        shared_context: dict[str, Any],
    ) -> SynthesisResult:
        value = self.responses.get("_synthesis", {})
        return SynthesisResult(
            proposal_version=task.proposal_version,
            round_number=int(shared_context["round_number"]),
            rationale=value.get("rationale", "No scripted revision was supplied."),
            proposal_changes=dict(value.get("proposal_changes", {})),
            changed_interfaces=list(value.get("changed_interfaces", [])),
            evidence_refs=list(value.get("evidence_refs", [])),
            addressed_objection_ids=list(value.get("addressed_objection_ids", [])),
            unresolved_objection_ids=list(value.get("unresolved_objection_ids", shared_context.get("open_objection_ids", []))),
        )


class HttpJsonProvider:
    """Provider-neutral JSON-over-HTTP adapter for an external model gateway.

    The gateway must authenticate, route models, construct the full canonical prompt,
    validate model output and return JSON matching the requested operation. The endpoint
    is explicit; this class has no default network destination.
    """

    name = "http-json"

    def __init__(
        self,
        endpoint: str,
        api_key: str | None = None,
        timeout_s: float = 120.0,
        repo_root: str | Path | None = None,
    ):
        if not endpoint.startswith(("https://", "http://localhost", "http://127.0.0.1")):
            raise ValueError("provider endpoint must use HTTPS or be localhost")
        self.endpoint = endpoint
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.repo_root = Path(repo_root).resolve() if repo_root else None
        self._document_cache: dict[str, dict[str, str]] = {}

    def assess_relevance(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        deterministic: AttendanceRecord,
    ) -> AttendanceRecord:
        value = self._post("assess_relevance", {
            "agent": self._agent_payload(agent, include_documents=False),
            "task": asdict(task),
            "deterministic_screen": _jsonable(asdict(deterministic)),
            "required_output_schema": self._output_schema("attendance-record"),
        })
        # A model may increase relevance, but never erase a deterministic safety net.
        proposed = deterministic.relevance.__class__(value.get("relevance", deterministic.relevance.value))
        if _relevance_rank(proposed) < _relevance_rank(deterministic.relevance):
            proposed = deterministic.relevance
        proposed_score = float(value.get("score", deterministic.score))
        if not math.isfinite(proposed_score) or proposed_score < 0:
            raise ValueError("provider relevance score must be finite and non-negative")
        return AttendanceRecord(
            agent_id=agent.agent_id,
            proposal_version=task.proposal_version,
            relevance=proposed,
            score=max(deterministic.score, proposed_score),
            mandatory=deterministic.mandatory,
            reasons=deterministic.reasons + list(value.get("reasons", [])),
            interfaces_affected=sorted(set(
                deterministic.interfaces_affected + list(value.get("interfaces_affected", []))
            )),
        )

    def analyze(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        shared_context: dict[str, Any],
    ) -> AgentPosition:
        value = self._post("independent_analysis", {
            "agent": self._agent_payload(agent, include_documents=True),
            "task": asdict(task),
            "shared_context": shared_context,
            "required_output_schema": self._output_schema("agent-position"),
        })
        if value.get("agent_id") not in (None, agent.agent_id):
            raise ValueError("provider returned a position for the wrong agent")
        confidence = float(value.get("confidence", 0.0))
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("provider confidence must be between 0 and 1")
        return AgentPosition(
            agent_id=agent.agent_id,
            proposal_version=task.proposal_version,
            verdict=Verdict(value["verdict"]),
            confidence=confidence,
            rationale=str(value.get("rationale", "")),
            claims=list(value.get("claims", [])),
            assumptions=list(value.get("assumptions", [])),
            risks=list(value.get("risks", [])),
            conditions=list(value.get("conditions", [])),
            evidence_refs=list(value.get("evidence_refs", [])),
            requested_agents=list(value.get("requested_agents", [])),
            verification=list(value.get("verification", [])),
        )

    def deliberate(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        shared_context: dict[str, Any],
    ) -> DeliberationContribution:
        value = self._post("deliberation", {
            "agent": self._agent_payload(agent, include_documents=True),
            "task": asdict(task),
            "shared_context": shared_context,
            "required_output_schema": self._output_schema("deliberation-contribution"),
        })
        return DeliberationContribution(
            agent_id=agent.agent_id,
            proposal_version=task.proposal_version,
            round_number=int(shared_context["round_number"]),
            rationale=str(value.get("rationale", "")),
            responses=list(value.get("responses", [])),
            counterarguments=list(value.get("counterarguments", [])),
            proposed_changes=dict(value.get("proposed_changes", {})),
            changed_interfaces=list(value.get("changed_interfaces", [])),
            evidence_refs=list(value.get("evidence_refs", [])),
            resolve_objection_ids=list(value.get("resolve_objection_ids", [])),
            requested_agents=list(value.get("requested_agents", [])),
        )

    def synthesize(
        self,
        agent: AgentConfig,
        task: TaskManifest,
        contributions: list[DeliberationContribution],
        shared_context: dict[str, Any],
    ) -> SynthesisResult:
        value = self._post("synthesis", {
            "agent": self._agent_payload(agent, include_documents=True),
            "task": asdict(task),
            "contributions": [asdict(item) for item in contributions],
            "shared_context": shared_context,
            "required_output_schema": self._output_schema("synthesis-result"),
        })
        return SynthesisResult(
            proposal_version=task.proposal_version,
            round_number=int(shared_context["round_number"]),
            rationale=str(value.get("rationale", "")),
            proposal_changes=dict(value.get("proposal_changes", {})),
            changed_interfaces=list(value.get("changed_interfaces", [])),
            evidence_refs=list(value.get("evidence_refs", [])),
            addressed_objection_ids=list(value.get("addressed_objection_ids", [])),
            unresolved_objection_ids=list(value.get("unresolved_objection_ids", [])),
        )

    def _post(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps({"operation": operation, "payload": payload}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        if self.api_key:
            request.add_header("Authorization", f"Bearer {self.api_key}")
        with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
            value = json.load(response)
        if not isinstance(value, dict):
            raise ValueError("provider response must be a JSON object")
        return value

    def _agent_payload(self, agent: AgentConfig, include_documents: bool) -> dict[str, Any]:
        payload: dict[str, Any] = {"configuration": asdict(agent)}
        if not include_documents:
            return payload
        if self.repo_root is None:
            raise ValueError("repo_root is required to embed canonical agent instructions")
        refs = list(dict.fromkeys(agent.mandatory_context + [agent.handbook]))
        payload["instruction_documents"] = [self._load_document(ref) for ref in refs]
        return payload

    def _load_document(self, relative_path: str) -> dict[str, str]:
        if relative_path in self._document_cache:
            return self._document_cache[relative_path]
        assert self.repo_root is not None
        source = (self.repo_root / relative_path).resolve()
        try:
            source.relative_to(self.repo_root)
        except ValueError as exc:
            raise ValueError(f"instruction path escapes repo root: {relative_path}") from exc
        content = source.read_text(encoding="utf-8")
        document = {
            "path": relative_path,
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "content": content,
        }
        self._document_cache[relative_path] = document
        return document

    def _output_schema(self, schema_name: str) -> dict[str, Any]:
        if self.repo_root is None:
            return {"title": schema_name}
        source = self.repo_root / "schemas" / "conference" / f"{schema_name}.schema.json"
        with source.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
        if not isinstance(value, dict):
            raise ValueError(f"output schema is not an object: {source}")
        return value


def _relevance_rank(value) -> int:
    return {"out_of_scope": 0, "monitor": 1, "affected": 2, "reviewer": 3, "primary": 4}[value.value]


def _jsonable(value: Any) -> Any:
    if hasattr(value, "value"):
        return value.value
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value
