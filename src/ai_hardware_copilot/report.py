"""Human-readable summary generated only from structured conference state."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from .models import ConferenceRecord


def write_report(record: ConferenceRecord, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    relevance = Counter(item.relevance.value for item in record.attendance.values())
    current_positions = [
        position for position in record.positions
        if position.proposal_version == record.task.proposal_version
    ]
    verdicts = Counter(position.verdict.value for position in current_positions)
    current_objections = [
        objection for objection in record.objections
        if objection.proposal_version == record.task.proposal_version
    ]
    lines = [
        f"# Engineering Conference {record.conference_id}",
        "",
        f"- **State:** `{record.state.value}`",
        f"- **Proposal version:** `{record.task.proposal_version}`",
        f"- **Task:** {record.task.title}",
        f"- **Objective:** {record.task.objective}",
        f"- **Agents screened:** {len(record.attendance)}",
        f"- **Active specialists:** {len(record.active_agents)}",
        f"- **Provider screening failures:** {len(record.screening_failures)}",
        f"- **Provider analysis failures:** {len(record.analysis_failures)}",
        "",
        "## Attendance",
        "",
        "| Relevance | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in sorted(relevance.items()))
    lines.extend([
        "",
        "### Complete attendance audit",
        "",
        "| Agent | Relevance | Mandatory | Score | Reasons |",
        "|---|---|---:|---:|---|",
    ])
    for agent_id, attendance in sorted(record.attendance.items()):
        reasons = "; ".join(attendance.reasons).replace("|", "\\|")
        lines.append(
            f"| {agent_id} | {attendance.relevance.value} | "
            f"{'yes' if attendance.mandatory else 'no'} | {attendance.score:.2f} | {reasons} |"
        )
    lines.extend(["", "## Active work cell", "", ", ".join(record.active_agents) or "None", ""])
    lines.extend(["## Current positions", "", "| Verdict | Count |", "|---|---:|"])
    lines.extend(f"| {key} | {value} |" for key, value in sorted(verdicts.items()))
    if current_positions:
        lines.extend([
            "",
            "### Specialist position audit",
            "",
            "| Agent | Verdict | Confidence | Evidence | Rationale |",
            "|---|---|---:|---|---|",
        ])
        for position in sorted(current_positions, key=lambda item: item.agent_id):
            evidence = ", ".join(position.evidence_refs).replace("|", "\\|") or "None"
            rationale = position.rationale.replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| {position.agent_id} | {position.verdict.value} | "
                f"{position.confidence:.2f} | {evidence} | {rationale} |"
            )
    lines.extend(["", "## Current objections", ""])
    if current_objections:
        lines.extend(["| ID | Agent | Severity | Status | Disputed claim |", "|---|---|---|---|---|"])
        for objection in current_objections:
            claim = objection.disputed_claim.replace("|", "\\|")
            lines.append(
                f"| {objection.objection_id} | {objection.agent_id} | "
                f"{objection.severity.value} | {objection.status} | {claim} |"
            )
    else:
        lines.append("None.")
    lines.extend(["", "## Coverage and convergence", ""])
    if record.coverage_report:
        lines.extend(["| Check | Result |", "|---|---|"])
        for check, passed in record.coverage_report.checks.items():
            lines.append(f"| {check} | {'PASS' if passed else 'FAIL'} |")
        if record.coverage_report.warnings:
            lines.extend(["", "Warnings:", ""])
            lines.extend(f"- {warning}" for warning in record.coverage_report.warnings)
    else:
        lines.append("Coverage has not been evaluated.")
    if record.final_decision:
        lines.extend(["", "## Final decision", "", record.final_decision["summary"]])
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination
