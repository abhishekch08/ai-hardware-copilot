"""Typed records used by the conference runtime.

The runtime deliberately persists conclusions, assumptions, evidence references and
objections. It does not request or store hidden model chain-of-thought.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import re
from typing import Any


class ConferenceState(str, Enum):
    INTAKE = "INTAKE"
    CONTEXT_FROZEN = "CONTEXT_FROZEN"
    ALL_AGENTS_SCREENED = "ALL_AGENTS_SCREENED"
    WORK_CELL_FORMED = "WORK_CELL_FORMED"
    INDEPENDENT_ANALYSIS = "INDEPENDENT_ANALYSIS"
    POSITIONS_COLLECTED = "POSITIONS_COLLECTED"
    OBJECTIONS_OPEN = "OBJECTIONS_OPEN"
    PROPOSAL_REVISED = "PROPOSAL_REVISED"
    AFFECTED_AGENTS_REACTIVATED = "AFFECTED_AGENTS_REACTIVATED"
    OBJECTIONS_RESOLVED = "OBJECTIONS_RESOLVED"
    VERIFIED = "VERIFIED"
    FINALIZED = "FINALIZED"
    BLOCKED = "BLOCKED"


class Relevance(str, Enum):
    PRIMARY = "primary"
    REVIEWER = "reviewer"
    AFFECTED = "affected"
    MONITOR = "monitor"
    OUT_OF_SCOPE = "out_of_scope"


class Verdict(str, Enum):
    APPROVE = "approve"
    APPROVE_WITH_CONDITIONS = "approve_with_conditions"
    OBJECT = "object"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    ABSTAIN_OUT_OF_SCOPE = "abstain_out_of_scope"


class Severity(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


@dataclass(slots=True)
class TaskManifest:
    task_id: str
    title: str
    objective: str
    description: str
    task_type: str = "new_product_design"
    risk_tier: str = "T2"
    domains: list[str] = field(default_factory=list)
    interfaces: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    excluded_keywords: list[str] = field(default_factory=list)
    required_agents: list[str] = field(default_factory=list)
    requirements: list[Any] = field(default_factory=list)
    constraints: list[Any] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    proposal: dict[str, Any] = field(default_factory=dict)
    proposal_version: int = 1
    physical_action: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "TaskManifest":
        unknown = set(value) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValueError(f"unknown TaskManifest fields: {sorted(unknown)}")
        required = ("task_id", "title", "objective", "description")
        missing = [key for key in required if not str(value.get(key, "")).strip()]
        if missing:
            raise ValueError(f"task manifest missing required fields: {', '.join(missing)}")
        task_id = str(value["task_id"])
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", task_id) is None:
            raise ValueError("task_id must be 1-96 path-safe letters, numbers, dots, underscores or hyphens")
        risk = str(value.get("risk_tier", "T2")).upper()
        if risk not in {"T0", "T1", "T2", "T3", "T4"}:
            raise ValueError(f"invalid risk_tier: {risk}")
        data = dict(value)
        data["risk_tier"] = risk
        return cls(**{key: data[key] for key in cls.__dataclass_fields__ if key in data})


@dataclass(slots=True)
class AgentConfig:
    agent_id: str
    name: str
    capability_level: str
    exact_specialization: str
    summary: str
    domains: list[str]
    activation_keywords: list[str]
    handbook: str
    mandatory_context: list[str]
    default_tools: list[str]
    can_block: list[str]
    status: str = "configured"

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "AgentConfig":
        unknown = set(value) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValueError(f"unknown AgentConfig fields: {sorted(unknown)}")
        return cls(**value)


@dataclass(slots=True)
class AttendanceRecord:
    agent_id: str
    proposal_version: int
    relevance: Relevance
    score: float
    mandatory: bool
    reasons: list[str] = field(default_factory=list)
    interfaces_affected: list[str] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AgentPosition:
    agent_id: str
    proposal_version: int
    verdict: Verdict
    confidence: float
    rationale: str
    claims: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    requested_agents: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Objection:
    objection_id: str
    agent_id: str
    proposal_version: int
    severity: Severity
    disputed_claim: str
    causal_mechanism: str
    required_resolution: str
    evidence_refs: list[str] = field(default_factory=list)
    status: str = "open"
    resolution: str | None = None
    resolved_by: str | None = None
    resolved_at: str | None = None


@dataclass(slots=True)
class DeliberationContribution:
    agent_id: str
    proposal_version: int
    round_number: int
    rationale: str
    responses: list[dict[str, Any]] = field(default_factory=list)
    counterarguments: list[str] = field(default_factory=list)
    proposed_changes: dict[str, Any] = field(default_factory=dict)
    changed_interfaces: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    resolve_objection_ids: list[str] = field(default_factory=list)
    requested_agents: list[str] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SynthesisResult:
    proposal_version: int
    round_number: int
    rationale: str
    proposal_changes: dict[str, Any] = field(default_factory=dict)
    changed_interfaces: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    addressed_objection_ids: list[str] = field(default_factory=list)
    unresolved_objection_ids: list[str] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ConferenceEvent:
    sequence: int
    timestamp_utc: str
    event_type: str
    actor: str
    proposal_version: int
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CoverageReport:
    passed: bool
    checks: dict[str, bool]
    failures: list[str]
    warnings: list[str]


@dataclass(slots=True)
class ConferenceRecord:
    conference_id: str
    state: ConferenceState
    task: TaskManifest
    attendance: dict[str, AttendanceRecord] = field(default_factory=dict)
    active_agents: list[str] = field(default_factory=list)
    required_agents: list[str] = field(default_factory=list)
    positions: list[AgentPosition] = field(default_factory=list)
    objections: list[Objection] = field(default_factory=list)
    deliberations: list[DeliberationContribution] = field(default_factory=list)
    syntheses: list[SynthesisResult] = field(default_factory=list)
    current_round: int = 0
    pending_review_agents: list[str] = field(default_factory=list)
    screening_failures: list[str] = field(default_factory=list)
    analysis_failures: list[str] = field(default_factory=list)
    events: list[ConferenceEvent] = field(default_factory=list)
    coverage_report: CoverageReport | None = None
    final_decision: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "ConferenceRecord":
        task = TaskManifest.from_dict(value["task"])
        attendance = {
            agent_id: AttendanceRecord(
                **{**item, "relevance": Relevance(item["relevance"])}
            )
            for agent_id, item in value.get("attendance", {}).items()
        }
        positions = [
            AgentPosition(**{**item, "verdict": Verdict(item["verdict"])})
            for item in value.get("positions", [])
        ]
        objections = [
            Objection(**{**item, "severity": Severity(item["severity"])})
            for item in value.get("objections", [])
        ]
        deliberations = [
            DeliberationContribution(**item) for item in value.get("deliberations", [])
        ]
        syntheses = [SynthesisResult(**item) for item in value.get("syntheses", [])]
        events = [ConferenceEvent(**item) for item in value.get("events", [])]
        coverage_value = value.get("coverage_report")
        coverage = CoverageReport(**coverage_value) if coverage_value else None
        return cls(
            conference_id=value["conference_id"],
            state=ConferenceState(value["state"]),
            task=task,
            attendance=attendance,
            active_agents=list(value.get("active_agents", [])),
            required_agents=list(value.get("required_agents", [])),
            positions=positions,
            objections=objections,
            deliberations=deliberations,
            syntheses=syntheses,
            current_round=int(value.get("current_round", 0)),
            pending_review_agents=list(value.get("pending_review_agents", [])),
            screening_failures=list(value.get("screening_failures", [])),
            analysis_failures=list(value.get("analysis_failures", [])),
            events=events,
            coverage_report=coverage,
            final_decision=value.get("final_decision"),
        )


def _enum_values(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _enum_values(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_enum_values(item) for item in value]
    return value
