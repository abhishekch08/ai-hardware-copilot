"""Evidence-gated product-design conference state machine."""

from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from .directory import AgentDirectory
from .models import (
    AgentPosition,
    AttendanceRecord,
    ConferenceEvent,
    ConferenceRecord,
    ConferenceState,
    CoverageReport,
    DeliberationContribution,
    Objection,
    Relevance,
    Severity,
    SynthesisResult,
    TaskManifest,
    Verdict,
)
from .provider import ReasoningProvider
from .routing import RoutingPolicy
from .storage import ConferenceStore


class InvalidTransition(RuntimeError):
    pass


class ConferenceEngine:
    """Runs a resumable structured conference.

    Consensus is not a vote. Finalization requires coverage, current-version reviews,
    resolved material objections, evidence gates and independent verification.
    """

    def __init__(
        self,
        directory: AgentDirectory,
        routing: RoutingPolicy,
        provider: ReasoningProvider,
        store: ConferenceStore | None = None,
        max_workers: int = 8,
    ):
        self.directory = directory
        self.routing = routing
        self.provider = provider
        self.store = store
        self.max_workers = max(1, max_workers)

    def create(self, task: TaskManifest) -> ConferenceRecord:
        record = ConferenceRecord(
            conference_id=f"CONF-{task.task_id}",
            state=ConferenceState.INTAKE,
            task=task,
        )
        self._event(record, "conference_created", "system", {"provider": self.provider.name})
        self._save(record)
        return record

    def freeze_context(self, record: ConferenceRecord) -> None:
        self._require(record, {ConferenceState.INTAKE, ConferenceState.PROPOSAL_REVISED})
        canonical = json.dumps(asdict(record.task), sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        record.task.metadata["context_sha256"] = digest
        record.state = ConferenceState.CONTEXT_FROZEN
        self._event(record, "context_frozen", "system", {"context_sha256": digest})
        self._save(record)

    def screen_all_agents(self, record: ConferenceRecord) -> None:
        self._require(record, {ConferenceState.CONTEXT_FROZEN})
        deterministic = self.routing.screen_all(record.task)
        assessed: dict[str, AttendanceRecord] = {}
        failures: list[str] = []

        def assess(agent_id: str) -> AttendanceRecord:
            result = self.provider.assess_relevance(
                self.directory.get(agent_id), record.task, deterministic[agent_id]
            )
            if result.agent_id != agent_id:
                raise ValueError(f"screen returned wrong agent_id {result.agent_id}")
            if result.proposal_version != record.task.proposal_version:
                raise ValueError("screen returned stale proposal_version")
            return result

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {pool.submit(assess, agent_id): agent_id for agent_id in sorted(self.directory.ids)}
            for future in as_completed(futures):
                agent_id = futures[future]
                try:
                    assessed[agent_id] = future.result()
                except Exception as exc:  # fail open for attendance, fail closed for release
                    fallback = deterministic[agent_id]
                    if fallback.relevance in {Relevance.MONITOR, Relevance.OUT_OF_SCOPE}:
                        fallback.relevance = Relevance.AFFECTED
                    fallback.reasons.append(f"reasoning-provider screening failed: {type(exc).__name__}")
                    assessed[agent_id] = fallback
                    failures.append(agent_id)

        record.attendance = dict(sorted(assessed.items()))
        record.screening_failures = failures
        record.active_agents = self.routing.active_agents(record.attendance)
        record.required_agents = sorted(
            agent_id for agent_id, attendance in record.attendance.items() if attendance.mandatory
        )
        record.pending_review_agents = list(record.active_agents)
        record.state = ConferenceState.ALL_AGENTS_SCREENED
        self._event(record, "all_agents_screened", "META-01", {
            "total": len(record.attendance),
            "active": len(record.active_agents),
            "mandatory": len(record.required_agents),
            "provider_failures": failures,
        })
        record.state = ConferenceState.WORK_CELL_FORMED
        self._event(record, "work_cell_formed", "META-01", {
            "active_agents": record.active_agents,
            "required_agents": record.required_agents,
        })
        self._save(record)

    def collect_independent_positions(self, record: ConferenceRecord) -> None:
        self._require(record, {
            ConferenceState.WORK_CELL_FORMED,
            ConferenceState.AFFECTED_AGENTS_REACTIVATED,
        })
        record.state = ConferenceState.INDEPENDENT_ANALYSIS
        version = record.task.proposal_version
        context = {
            "conference_id": record.conference_id,
            "context_sha256": record.task.metadata.get("context_sha256"),
            "proposal_version": version,
            "evidence_refs": record.task.evidence_refs,
            "independence_rule": "Do not use other agents' positions in this pass.",
        }
        positions: dict[str, AgentPosition] = {}
        failures: list[str] = []

        def analyze(agent_id: str) -> AgentPosition:
            result = self.provider.analyze(self.directory.get(agent_id), record.task, context)
            if result.agent_id != agent_id:
                raise ValueError(f"analysis returned wrong agent_id {result.agent_id}")
            if result.proposal_version != version:
                raise ValueError("analysis returned stale proposal_version")
            if not 0.0 <= result.confidence <= 1.0:
                raise ValueError("confidence must be between 0 and 1")
            unknown_requests = set(result.requested_agents) - self.directory.ids
            if unknown_requests:
                raise ValueError(f"analysis requested unknown agents: {sorted(unknown_requests)}")
            self._validate_evidence_refs(record, result.evidence_refs)
            if (
                int(record.task.risk_tier[1:]) >= 3
                and result.verdict in {Verdict.APPROVE, Verdict.APPROVE_WITH_CONDITIONS}
                and not result.evidence_refs
            ):
                raise ValueError("T3/T4 approval requires registered evidence")
            return result

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {pool.submit(analyze, agent_id): agent_id for agent_id in record.active_agents}
            for future in as_completed(futures):
                agent_id = futures[future]
                try:
                    positions[agent_id] = future.result()
                except Exception as exc:
                    failures.append(agent_id)
                    positions[agent_id] = AgentPosition(
                        agent_id=agent_id,
                        proposal_version=version,
                        verdict=Verdict.INSUFFICIENT_EVIDENCE,
                        confidence=0.0,
                        rationale=f"Analysis provider failed: {type(exc).__name__}",
                        risks=["No valid specialist analysis was received."],
                        conditions=["Retry this specialist before convergence."],
                    )

        # Keep prior revisions for audit; replace only same-agent same-version retries.
        retained = [p for p in record.positions if p.proposal_version != version or p.agent_id not in positions]
        record.positions = retained + [positions[key] for key in sorted(positions)]
        record.analysis_failures = failures
        requested = sorted({
            requested_id
            for position in positions.values()
            for requested_id in position.requested_agents
        })
        newly_active = [agent_id for agent_id in requested if agent_id not in record.active_agents]
        if newly_active:
            record.active_agents = sorted(set(record.active_agents) | set(newly_active))
            record.required_agents = sorted(set(record.required_agents) | set(newly_active))
            record.pending_review_agents = newly_active
            record.state = ConferenceState.AFFECTED_AGENTS_REACTIVATED
            self._event(record, "specialists_requested", "META-01", {"agents": newly_active})
            self._save(record)
            self.collect_independent_positions(record)
            return

        record.pending_review_agents = []
        record.state = ConferenceState.POSITIONS_COLLECTED
        self._event(record, "independent_positions_collected", "system", {
            "proposal_version": version,
            "positions": len(positions),
            "provider_failures": failures,
        })
        self._derive_objections(record, positions.values())
        self._save(record)

    def _derive_objections(self, record: ConferenceRecord, positions) -> None:
        version = record.task.proposal_version
        record.objections = [
            objection for objection in record.objections
            if not (objection.proposal_version == version and objection.status == "open")
        ]
        next_index = len(record.objections) + 1
        for position in positions:
            items: list[tuple[Severity, str, str]] = []
            if position.verdict is Verdict.OBJECT:
                severity = Severity.CRITICAL if (
                    int(record.task.risk_tier[1:]) >= 3
                    and bool(self.directory.get(position.agent_id).can_block)
                ) else Severity.MAJOR
                claim = position.risks[0] if position.risks else "Specialist objects to the proposal."
                items.append((severity, claim, position.rationale))
            elif position.verdict is Verdict.INSUFFICIENT_EVIDENCE:
                items.append((Severity.MAJOR, "Evidence is insufficient for specialist approval.", position.rationale))
            elif position.verdict is Verdict.APPROVE_WITH_CONDITIONS:
                for condition in position.conditions or ["Conditional approval requires resolution."]:
                    items.append((Severity.MINOR, condition, position.rationale))

            for severity, claim, mechanism in items:
                record.objections.append(Objection(
                    objection_id=f"OBJ-{version:03d}-{next_index:04d}",
                    agent_id=position.agent_id,
                    proposal_version=version,
                    severity=severity,
                    disputed_claim=claim,
                    causal_mechanism=mechanism,
                    required_resolution=(position.conditions[0] if position.conditions else "Provide evidence or revise the proposal."),
                    evidence_refs=list(position.evidence_refs),
                ))
                next_index += 1

        open_count = sum(o.status == "open" for o in record.objections)
        record.state = ConferenceState.OBJECTIONS_OPEN if open_count else ConferenceState.OBJECTIONS_RESOLVED
        self._event(record, "objections_derived", "META-04", {"open": open_count})

    def resolve_objection(
        self,
        record: ConferenceRecord,
        objection_id: str,
        resolution: str,
        resolved_by: str,
        evidence_refs: list[str] | None = None,
    ) -> None:
        objection = next((item for item in record.objections if item.objection_id == objection_id), None)
        if objection is None:
            raise KeyError(f"unknown objection_id: {objection_id}")
        if objection.status == "resolved":
            raise ValueError(f"objection already resolved: {objection_id}")
        if resolved_by not in {objection.agent_id, "HUMAN-AUTHORITY"}:
            raise ValueError("objection resolution must be confirmed by its owner or HUMAN-AUTHORITY")
        evidence_refs = evidence_refs or []
        if objection.severity in {Severity.CRITICAL, Severity.MAJOR} and not evidence_refs:
            raise ValueError("major/critical objection resolution requires evidence_refs")
        if not resolution.strip():
            raise ValueError("resolution cannot be empty")
        self._validate_evidence_refs(record, evidence_refs)
        objection.status = "resolved"
        objection.resolution = resolution.strip()
        objection.resolved_by = resolved_by
        objection.resolved_at = _now()
        objection.evidence_refs = sorted(set(objection.evidence_refs + evidence_refs))
        self._event(record, "objection_resolved", resolved_by, {
            "objection_id": objection_id,
            "evidence_refs": evidence_refs,
        })
        if not self._open_objections(record):
            record.state = ConferenceState.OBJECTIONS_RESOLVED
        self._save(record)

    def revise_proposal(
        self,
        record: ConferenceRecord,
        changes: dict[str, Any],
        changed_interfaces: list[str],
        evidence_refs: list[str],
        actor: str = "META-03",
    ) -> None:
        self._require(record, {
            ConferenceState.POSITIONS_COLLECTED,
            ConferenceState.OBJECTIONS_OPEN,
            ConferenceState.OBJECTIONS_RESOLVED,
            ConferenceState.BLOCKED,
        })
        if not changes:
            raise ValueError("proposal revision must contain changes")
        old_version = record.task.proposal_version
        record.task.proposal = _deep_merge(record.task.proposal, changes)
        record.task.interfaces = sorted(set(record.task.interfaces + changed_interfaces))
        record.task.evidence_refs = sorted(set(record.task.evidence_refs + evidence_refs))
        record.task.proposal_version += 1
        for objection in record.objections:
            if objection.status == "open":
                objection.status = "superseded_pending_review"
        record.state = ConferenceState.PROPOSAL_REVISED
        self._event(record, "proposal_revised", actor, {
            "from_version": old_version,
            "to_version": record.task.proposal_version,
            "changes": changes,
            "changed_interfaces": changed_interfaces,
            "evidence_refs": evidence_refs,
        })
        self.freeze_context(record)
        self.screen_all_agents(record)
        record.state = ConferenceState.AFFECTED_AGENTS_REACTIVATED
        record.pending_review_agents = list(record.active_agents)
        self._event(record, "agents_reactivated_after_revision", "META-01", {
            "proposal_version": record.task.proposal_version,
            "agents": record.active_agents,
        })
        self._save(record)

    def deliberate_round(self, record: ConferenceRecord) -> bool:
        """Run one visible objection/rebuttal/synthesis round.

        Returns True when a new proposal version was created. A provider cannot resolve
        another specialist's objection; only the objection owner may confirm it, and
        major/critical resolutions require evidence.
        """
        self._require(record, {ConferenceState.OBJECTIONS_OPEN})
        open_objections = self._open_objections(record)
        if not open_objections:
            record.state = ConferenceState.OBJECTIONS_RESOLVED
            self._save(record)
            return False

        record.current_round += 1
        round_number = record.current_round
        version = record.task.proposal_version
        serialized = record.as_dict()
        current_positions = [
            position for position in serialized["positions"] if position["proposal_version"] == version
        ]
        serialized_objections = {
            item["objection_id"]: item for item in serialized["objections"]
        }
        context = {
            "round_number": round_number,
            "proposal_version": version,
            "open_objections": [serialized_objections[item.objection_id] for item in open_objections],
            "open_objection_ids": [item.objection_id for item in open_objections],
            "current_positions": current_positions,
            "evidence_refs": record.task.evidence_refs,
            "rule": "Respond to claims and evidence; do not vote or repeat unsupported assertions.",
        }
        contributions: dict[str, DeliberationContribution] = {}
        failures: list[str] = []

        def contribute(agent_id: str) -> DeliberationContribution:
            value = self.provider.deliberate(self.directory.get(agent_id), record.task, context)
            if value.agent_id != agent_id:
                raise ValueError("deliberation returned wrong agent_id")
            if value.proposal_version != version or value.round_number != round_number:
                raise ValueError("deliberation returned stale version or round")
            if set(value.resolve_objection_ids) - set(context["open_objection_ids"]):
                raise ValueError("deliberation referenced an unknown/currently closed objection")
            if set(value.requested_agents) - self.directory.ids:
                raise ValueError("deliberation requested an unknown agent")
            self._validate_evidence_refs(record, value.evidence_refs)
            return value

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {pool.submit(contribute, agent_id): agent_id for agent_id in record.active_agents}
            for future in as_completed(futures):
                agent_id = futures[future]
                try:
                    contributions[agent_id] = future.result()
                except Exception as exc:
                    failures.append(agent_id)
                    self._event(record, "deliberation_provider_failure", agent_id, {
                        "error_type": type(exc).__name__, "round_number": round_number,
                    })

        record.analysis_failures = sorted(set(record.analysis_failures + failures))
        record.deliberations.extend(contributions[key] for key in sorted(contributions))
        self._event(record, "deliberation_round_collected", "system", {
            "round_number": round_number,
            "contributions": len(contributions),
            "failures": failures,
        })

        # An objection owner may explicitly confirm resolution based on cited evidence.
        by_id = {item.objection_id: item for item in record.objections}
        for contribution in contributions.values():
            for objection_id in contribution.resolve_objection_ids:
                objection = by_id[objection_id]
                if contribution.agent_id != objection.agent_id:
                    continue
                if objection.severity in {Severity.CRITICAL, Severity.MAJOR} and not contribution.evidence_refs:
                    continue
                objection.status = "resolved"
                objection.resolution = contribution.rationale
                objection.resolved_by = contribution.agent_id
                objection.resolved_at = _now()
                objection.evidence_refs = sorted(set(objection.evidence_refs + contribution.evidence_refs))
                self._event(record, "objection_resolved_by_owner", contribution.agent_id, {
                    "objection_id": objection_id,
                    "round_number": round_number,
                })

        requested = sorted({
            agent_id for contribution in contributions.values() for agent_id in contribution.requested_agents
        })
        newly_active = [agent_id for agent_id in requested if agent_id not in record.active_agents]
        if newly_active:
            record.active_agents = sorted(set(record.active_agents) | set(newly_active))
            record.required_agents = sorted(set(record.required_agents) | set(newly_active))
            record.pending_review_agents = newly_active
            record.state = ConferenceState.AFFECTED_AGENTS_REACTIVATED
            self._event(record, "specialists_requested_during_deliberation", "META-01", {
                "agents": newly_active, "round_number": round_number,
            })
            self._save(record)
            self.collect_independent_positions(record)
            return False

        if not self._open_objections(record):
            record.state = ConferenceState.OBJECTIONS_RESOLVED
            self._event(record, "all_objections_resolved", "system", {"round_number": round_number})
            self._save(record)
            return False

        synthesis_context = {
            "round_number": round_number,
            "proposal_version": version,
            "open_objection_ids": [item.objection_id for item in self._open_objections(record)],
            "evidence_refs": record.task.evidence_refs,
        }
        try:
            synthesis = self.provider.synthesize(
                self.directory.get("META-03"),
                record.task,
                [contributions[key] for key in sorted(contributions)],
                synthesis_context,
            )
            self._validate_synthesis(synthesis, version, round_number, record)
        except Exception as exc:
            record.analysis_failures = sorted(set(record.analysis_failures + ["META-03"]))
            record.state = ConferenceState.BLOCKED
            self._event(record, "synthesis_provider_failure", "META-03", {
                "error_type": type(exc).__name__, "round_number": round_number,
            })
            self._save(record)
            return False

        record.syntheses.append(synthesis)
        self._event(record, "revision_synthesized", "META-03", {
            "round_number": round_number,
            "rationale": synthesis.rationale,
            "addressed_objection_ids": synthesis.addressed_objection_ids,
            "unresolved_objection_ids": synthesis.unresolved_objection_ids,
        })
        if not synthesis.proposal_changes:
            record.state = ConferenceState.BLOCKED
            self._event(record, "iteration_blocked_no_defensible_revision", "META-03", {
                "round_number": round_number,
                "open_objection_ids": synthesis_context["open_objection_ids"],
            })
            self._save(record)
            return False

        self.revise_proposal(
            record,
            changes=synthesis.proposal_changes,
            changed_interfaces=synthesis.changed_interfaces,
            evidence_refs=synthesis.evidence_refs,
            actor="META-03",
        )
        self.collect_independent_positions(record)
        return True

    def iterate(self, record: ConferenceRecord, max_rounds: int = 3) -> ConferenceRecord:
        if max_rounds < 1:
            raise ValueError("max_rounds must be at least 1")
        rounds_run = 0
        while record.state == ConferenceState.OBJECTIONS_OPEN and rounds_run < max_rounds:
            self.deliberate_round(record)
            rounds_run += 1
        if record.state == ConferenceState.OBJECTIONS_OPEN:
            record.state = ConferenceState.BLOCKED
            self._event(record, "iteration_limit_reached", "system", {
                "max_rounds": max_rounds,
                "open_objections": [item.objection_id for item in self._open_objections(record)],
            })
        self.coverage(record)
        self._save(record)
        return record

    def coverage(self, record: ConferenceRecord) -> CoverageReport:
        version = record.task.proposal_version
        current_positions = {p.agent_id: p for p in record.positions if p.proposal_version == version}
        open_objections = self._open_objections(record)
        risk = int(record.task.risk_tier[1:])
        checks = {
            "all_agents_screened": len(record.attendance) == len(self.directory),
            "screens_current": all(a.proposal_version == version for a in record.attendance.values()),
            "screening_provider_healthy": not record.screening_failures,
            "all_required_active": set(record.required_agents) <= set(record.active_agents),
            "all_active_reviewed_current_version": set(record.active_agents) <= set(current_positions),
            "analysis_provider_healthy": not record.analysis_failures,
            "no_objections_open": not open_objections,
            "independent_critic_present": risk < 2 or "META-04" in current_positions,
            "verification_agent_present": risk < 2 or bool({"AI-13", "TEST-03"} & set(current_positions)),
            "high_risk_has_evidence": risk < 3 or bool(record.task.evidence_refs),
            "high_risk_approvals_evidence_backed": risk < 3 or all(
                bool(position.evidence_refs)
                for position in current_positions.values()
                if position.agent_id in record.active_agents
                and position.verdict in {Verdict.APPROVE, Verdict.APPROVE_WITH_CONDITIONS}
            ),
            "no_active_agent_abstained": all(
                position.verdict is not Verdict.ABSTAIN_OUT_OF_SCOPE
                for position in current_positions.values()
                if position.agent_id in record.active_agents
            ),
        }
        failures = [name for name, passed in checks.items() if not passed]
        warnings = []
        if any(p.confidence < 0.5 for p in current_positions.values()):
            warnings.append("one or more current specialist positions have confidence below 0.5")
        report = CoverageReport(passed=not failures, checks=checks, failures=failures, warnings=warnings)
        record.coverage_report = report
        return report

    def finalize(
        self,
        record: ConferenceRecord,
        summary: str,
        accepted_residual_risks: list[str] | None = None,
    ) -> CoverageReport:
        report = self.coverage(record)
        if not report.passed:
            record.state = ConferenceState.BLOCKED
            self._event(record, "finalization_blocked", "META-05", {"failures": report.failures})
            self._save(record)
            return report
        record.state = ConferenceState.VERIFIED
        self._event(record, "conference_verified", "META-05", {"checks": report.checks})
        record.final_decision = {
            "proposal_version": record.task.proposal_version,
            "summary": summary,
            "accepted_residual_risks": accepted_residual_risks or [],
            "evidence_refs": list(record.task.evidence_refs),
            "finalized_at": _now(),
        }
        record.state = ConferenceState.FINALIZED
        self._event(record, "conference_finalized", "META-03", record.final_decision)
        self._save(record)
        return report

    def run_initial(self, task: TaskManifest) -> ConferenceRecord:
        record = self.create(task)
        self.freeze_context(record)
        self.screen_all_agents(record)
        self.collect_independent_positions(record)
        self.coverage(record)
        self._save(record)
        return record

    def _open_objections(self, record: ConferenceRecord) -> list[Objection]:
        return [
            objection for objection in record.objections
            if objection.proposal_version == record.task.proposal_version
            and objection.status != "resolved"
        ]

    def _validate_synthesis(
        self,
        synthesis: SynthesisResult,
        version: int,
        round_number: int,
        record: ConferenceRecord,
    ) -> None:
        if synthesis.proposal_version != version or synthesis.round_number != round_number:
            raise ValueError("synthesis returned stale proposal version or round")
        current_ids = {item.objection_id for item in self._open_objections(record)}
        referenced = set(synthesis.addressed_objection_ids) | set(synthesis.unresolved_objection_ids)
        if referenced - current_ids:
            raise ValueError("synthesis references an unknown/currently closed objection")
        if synthesis.proposal_changes and not synthesis.changed_interfaces:
            raise ValueError("a synthesized proposal change must declare changed interfaces")
        self._validate_evidence_refs(record, synthesis.evidence_refs)

    @staticmethod
    def _validate_evidence_refs(record: ConferenceRecord, evidence_refs: list[str]) -> None:
        """Reject citations that were not registered in the frozen task context.

        This proves identity/provenance, not semantic support. A future evidence service
        must additionally verify hashes, revisions, access and claim-to-source entailment.
        """
        unknown = set(evidence_refs) - set(record.task.evidence_refs)
        if unknown:
            raise ValueError(f"unregistered evidence_refs: {sorted(unknown)}")

    def _event(self, record: ConferenceRecord, event_type: str, actor: str, payload: dict[str, Any]) -> None:
        record.events.append(ConferenceEvent(
            sequence=len(record.events) + 1,
            timestamp_utc=_now(),
            event_type=event_type,
            actor=actor,
            proposal_version=record.task.proposal_version,
            payload=payload,
        ))

    def _save(self, record: ConferenceRecord) -> None:
        if self.store:
            self.store.save(record)

    @staticmethod
    def _require(record: ConferenceRecord, allowed: set[ConferenceState]) -> None:
        if record.state not in allowed:
            names = ", ".join(sorted(state.value for state in allowed))
            raise InvalidTransition(f"state {record.state.value} not in allowed states: {names}")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _deep_merge(base: dict[str, Any], changes: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in changes.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result
