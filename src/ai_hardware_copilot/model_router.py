"""Deterministic compute-profile selection for provider-neutral model gateways."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .models import TaskManifest


@dataclass(slots=True)
class ModelRoute:
    profile: str
    reasoning: str
    independent_review: bool
    model_diversity: bool
    reasons: list[str]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ModelRoutingPolicy:
    """Selects difficulty, never a vendor or a marketing model name."""

    def __init__(self, configuration: dict[str, Any]):
        self.profiles = dict(configuration.get("profiles", {}))
        required = {"deterministic", "standard", "deep", "maximum"}
        missing = required - set(self.profiles)
        if missing:
            raise ValueError(f"model profiles missing: {sorted(missing)}")

    def select(
        self,
        task: TaskManifest,
        operation: str,
        *,
        active_agent_count: int = 1,
    ) -> ModelRoute:
        risk = int(task.risk_tier[1:])
        reasons: list[str] = []
        if operation in {"schema_validation", "configuration_diff", "exact_lookup"}:
            profile = "deterministic"
            reasons.append("operation is deterministic")
        elif operation == "assess_relevance":
            profile = "deep" if risk >= 4 else "standard"
            reasons.append("bounded relevance classification")
        elif risk >= 4:
            profile = "maximum"
            reasons.append("T4 consequence requires maximum reasoning")
        elif operation in {"synthesis", "deliberation"} and risk >= 3:
            profile = "maximum"
            reasons.append("high-risk cross-agent reconciliation")
        elif risk >= 2 or len(task.domains) >= 3 or active_agent_count >= 12:
            profile = "deep"
            reasons.append("consequential or cross-domain engineering task")
        else:
            profile = "standard"
            reasons.append("bounded low-consequence reasoning task")

        config = self.profiles[profile]
        independent = config.get("independent_review") in {True, "true", "required"}
        if risk >= 2:
            independent = True
        diversity = bool(config.get("model_diversity", False)) or risk >= 4
        return ModelRoute(
            profile=profile,
            reasoning=str(config.get("reasoning", "medium")),
            independent_review=independent,
            model_diversity=diversity,
            reasons=reasons,
        )
