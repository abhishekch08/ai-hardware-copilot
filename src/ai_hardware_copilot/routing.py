"""All-agent screening, mandatory routing and coverage expansion."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from .directory import AgentDirectory
from .models import AttendanceRecord, Relevance, TaskManifest


_STOPWORDS = {
    "a", "an", "and", "agent", "are", "as", "at", "be", "build", "builds", "by",
    "current", "data", "design", "device", "evidence", "exact", "for", "from",
    "hardware", "in", "interface", "interfaces", "is", "it", "model", "new", "of",
    "on", "or", "owns", "primary", "product", "relevant", "required", "requirements",
    "review", "safe", "support", "supports", "system", "systems", "technical", "that",
    "the", "this", "to", "user", "users", "with", "work", "working",
}


def tokens(value: Any) -> set[str]:
    if isinstance(value, (list, tuple, set)):
        value = " ".join(str(item) for item in value)
    elif isinstance(value, dict):
        value = " ".join(f"{key} {item}" for key, item in value.items())
    words = set(re.findall(r"[a-z0-9]+", str(value).lower()))
    return {word for word in words if len(word) > 1 and word not in _STOPWORDS}


class RoutingPolicy:
    """Deterministic routing is the first safety net, not the final expert judgment."""

    def __init__(
        self,
        directory: AgentDirectory,
        review_rules: dict[str, Any],
        capability_graph: dict[str, Any],
    ):
        self.directory = directory
        self.rules = list(review_rules.get("rules", []))
        self.graph = capability_graph
        self._validate_references()

    def _validate_references(self) -> None:
        referenced: set[str] = set()
        for rule in self.rules:
            referenced.update((rule.get("include") or {}).keys())
        for source, targets in (self.graph.get("agent_edges") or {}).items():
            referenced.add(source)
            referenced.update(targets)
        referenced.update((self.graph.get("domain_leads") or {}).values())
        unknown = referenced - self.directory.ids
        if unknown:
            raise ValueError(f"routing config references unknown agents: {sorted(unknown)}")

    def mandatory_assignments(self, task: TaskManifest) -> tuple[dict[str, Relevance], dict[str, list[str]]]:
        assignments: dict[str, Relevance] = {}
        reasons: dict[str, list[str]] = defaultdict(list)
        for rule in self.rules:
            if not self._rule_matches(rule, task):
                continue
            for agent_id, relevance_text in (rule.get("include") or {}).items():
                relevance = Relevance(relevance_text)
                current = assignments.get(agent_id)
                if current is None or _relevance_rank(relevance) > _relevance_rank(current):
                    assignments[agent_id] = relevance
                reasons[agent_id].append(f"mandatory rule: {rule['id']}")

        # Exact agents named by the user/task are always activated.
        haystack = " ".join((task.description, task.objective, " ".join(task.keywords))).upper()
        for agent_id in self.directory.ids:
            if re.search(rf"\b{re.escape(agent_id)}\b", haystack):
                assignments[agent_id] = Relevance.PRIMARY
                reasons[agent_id].append("agent explicitly named in task")

        unknown_required = set(task.required_agents) - self.directory.ids
        if unknown_required:
            raise ValueError(f"task requires unknown agents: {sorted(unknown_required)}")
        for agent_id in task.required_agents:
            current = assignments.get(agent_id)
            if current is None or _relevance_rank(Relevance.REVIEWER) > _relevance_rank(current):
                assignments[agent_id] = Relevance.REVIEWER
            reasons[agent_id].append("agent required by task manifest")

        return assignments, reasons

    def _rule_matches(self, rule: dict[str, Any], task: TaskManifest) -> bool:
        task_tokens = self.task_tokens(task)
        if rule.get("task_types") and task.task_type not in set(rule["task_types"]):
            return False
        if rule.get("domains_any") and not set(rule["domains_any"]) & set(task.domains):
            return False
        if rule.get("interfaces_any") and not set(rule["interfaces_any"]) & set(task.interfaces):
            return False
        if rule.get("keywords_any") and not tokens(rule["keywords_any"]) & task_tokens:
            return False
        if rule.get("keywords_all") and not tokens(rule["keywords_all"]) <= task_tokens:
            return False
        if rule.get("risk_at_least"):
            if int(task.risk_tier[1:]) < int(str(rule["risk_at_least"])[1:]):
                return False
        if rule.get("physical_action") is not None and bool(rule["physical_action"]) != task.physical_action:
            return False
        return True

    def task_tokens(self, task: TaskManifest) -> set[str]:
        positive = tokens([
            task.title,
            task.objective,
            task.description,
            task.task_type,
            task.domains,
            task.interfaces,
            task.keywords,
            task.requirements,
            task.constraints,
            task.proposal,
        ])
        return positive - tokens(task.excluded_keywords)

    def screen_all(self, task: TaskManifest) -> dict[str, AttendanceRecord]:
        mandatory, mandatory_reasons = self.mandatory_assignments(task)
        task_tokens = self.task_tokens(task)
        task_domains = set(task.domains)
        task_interfaces = set(task.interfaces)
        records: dict[str, AttendanceRecord] = {}

        for agent in self.directory:
            agent_tokens = tokens([
                agent.name,
                agent.exact_specialization,
                agent.summary,
                agent.activation_keywords,
                agent.domains,
            ])
            overlap = sorted(task_tokens & agent_tokens)
            domain_overlap = sorted(task_domains & set(agent.domains))
            interface_overlap = sorted(task_interfaces & agent_tokens)
            score = min(12.0, 1.25 * len(overlap))
            score += 1.5 * len(domain_overlap)
            score += 2.0 * len(interface_overlap)
            reasons: list[str] = []
            if overlap:
                reasons.append(f"capability terms: {', '.join(overlap[:10])}")
            if domain_overlap:
                reasons.append(f"task domain: {', '.join(domain_overlap)}")
            if interface_overlap:
                reasons.append(f"affected interface: {', '.join(interface_overlap)}")

            if agent.agent_id in mandatory:
                relevance = mandatory[agent.agent_id]
                reasons.extend(mandatory_reasons[agent.agent_id])
            elif score >= 9:
                relevance = Relevance.PRIMARY
            elif score >= 5:
                relevance = Relevance.AFFECTED
            elif score >= 2 or domain_overlap:
                relevance = Relevance.MONITOR
            else:
                relevance = Relevance.OUT_OF_SCOPE

            records[agent.agent_id] = AttendanceRecord(
                agent_id=agent.agent_id,
                proposal_version=task.proposal_version,
                relevance=relevance,
                score=round(score, 2),
                mandatory=agent.agent_id in mandatory,
                reasons=reasons or ["no task-to-capability match"],
                interfaces_affected=interface_overlap,
            )

        self._expand_dependencies(records)
        return records

    def _expand_dependencies(self, records: dict[str, AttendanceRecord]) -> None:
        active = {
            agent_id for agent_id, record in records.items()
            if record.relevance in {Relevance.PRIMARY, Relevance.REVIEWER, Relevance.AFFECTED}
        }
        edges = self.graph.get("agent_edges") or {}
        additions: dict[str, list[str]] = defaultdict(list)
        for source in sorted(active):
            for target in edges.get(source, []):
                additions[target].append(source)

        active_domains = {
            domain
            for agent_id in active
            for domain in self.directory.get(agent_id).domains
        }
        domain_neighbors = self.graph.get("domain_neighbors") or {}
        domain_leads = self.graph.get("domain_leads") or {}
        for domain in sorted(active_domains):
            for neighbor in domain_neighbors.get(domain, []):
                lead = domain_leads.get(neighbor)
                if lead:
                    additions[lead].append(f"{domain} interface")

        for target, sources in additions.items():
            record = records[target]
            if record.relevance in {Relevance.MONITOR, Relevance.OUT_OF_SCOPE}:
                record.relevance = Relevance.REVIEWER
            record.mandatory = True
            record.reasons.append(f"dependency expansion from: {', '.join(sources[:8])}")

    @staticmethod
    def active_agents(records: dict[str, AttendanceRecord]) -> list[str]:
        return sorted(
            agent_id for agent_id, record in records.items()
            if record.relevance in {Relevance.PRIMARY, Relevance.REVIEWER, Relevance.AFFECTED}
        )


def _relevance_rank(value: Relevance) -> int:
    return {
        Relevance.OUT_OF_SCOPE: 0,
        Relevance.MONITOR: 1,
        Relevance.AFFECTED: 2,
        Relevance.REVIEWER: 3,
        Relevance.PRIMARY: 4,
    }[value]
