"""Evidence-updated hypotheses and information-gain experiment selection."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

from .evidence import EvidenceStore


@dataclass(slots=True)
class Hypothesis:
    hypothesis_id: str
    mechanism: str
    probability: float
    status: str = "open"


@dataclass(slots=True)
class CandidateExperiment:
    experiment_id: str
    question: str
    outcomes: list[str]
    likelihoods: dict[str, dict[str, float]]
    time_cost: float = 1.0
    risk_cost: float = 0.0
    monetary_cost: float = 0.0


@dataclass(slots=True)
class DiagnosticStep:
    experiment_id: str
    expected_information_gain_bits: float
    utility: float
    observed_outcome: str
    evidence_ref: str
    posterior: dict[str, float]


@dataclass(slots=True)
class DiagnosticSession:
    session_id: str
    hypotheses: list[Hypothesis]
    experiments: list[CandidateExperiment]
    steps: list[DiagnosticStep] = field(default_factory=list)
    status: str = "investigating"

    def probabilities(self) -> dict[str, float]:
        return {item.hypothesis_id: item.probability for item in self.hypotheses}


class ExperimentPlanner:
    def rank(
        self,
        hypotheses: list[Hypothesis],
        experiments: list[CandidateExperiment],
        completed: set[str] | None = None,
    ) -> list[tuple[CandidateExperiment, float, float]]:
        completed = completed or set()
        prior = _normalized({item.hypothesis_id: item.probability for item in hypotheses if item.status == "open"})
        result = []
        for experiment in experiments:
            if experiment.experiment_id in completed:
                continue
            information_gain = expected_information_gain(prior, experiment)
            cost = experiment.time_cost + experiment.risk_cost + experiment.monetary_cost
            utility = information_gain / max(cost, 1e-9)
            result.append((experiment, information_gain, utility))
        return sorted(result, key=lambda item: (-item[2], -item[1], item[0].experiment_id))

    def choose(
        self,
        hypotheses: list[Hypothesis],
        experiments: list[CandidateExperiment],
        completed: set[str] | None = None,
    ) -> tuple[CandidateExperiment, float, float]:
        ranked = self.rank(hypotheses, experiments, completed)
        if not ranked:
            raise ValueError("no candidate experiment remains")
        return ranked[0]


class DiagnosticEngine:
    def __init__(self, evidence: EvidenceStore, planner: ExperimentPlanner | None = None):
        self.evidence = evidence
        self.planner = planner or ExperimentPlanner()

    def run(
        self,
        session: DiagnosticSession,
        observe: Callable[[CandidateExperiment], tuple[str, dict[str, Any]]],
        *,
        confidence_threshold: float = 0.95,
        max_steps: int = 10,
    ) -> DiagnosticSession:
        if not 0.5 < confidence_threshold < 1:
            raise ValueError("confidence_threshold must be between 0.5 and 1")
        _validate_session(session)
        completed = {step.experiment_id for step in session.steps}
        for _ in range(max_steps):
            winner = max(session.hypotheses, key=lambda item: item.probability)
            if winner.probability >= confidence_threshold:
                winner.status = "confirmed_candidate"
                session.status = "root_cause_candidate"
                return session
            experiment, information_gain, utility = self.planner.choose(
                session.hypotheses, session.experiments, completed
            )
            outcome, measurement = observe(experiment)
            if outcome not in experiment.outcomes:
                raise ValueError(f"experiment returned undeclared outcome: {outcome}")
            prior = session.probabilities()
            posterior = bayesian_update(prior, experiment, outcome)
            evidence_record = self.evidence.register_json(
                {
                    "session_id": session.session_id,
                    "experiment": asdict(experiment),
                    "prior": prior,
                    "observed_outcome": outcome,
                    "measurement": measurement,
                    "posterior": posterior,
                },
                kind="diagnostic_experiment",
                source_uri=f"diagnostic://{session.session_id}/{experiment.experiment_id}",
                configuration=measurement.get("configuration", {}),
                derived_from=list(measurement.get("evidence_refs", [])),
            )
            for hypothesis in session.hypotheses:
                hypothesis.probability = posterior[hypothesis.hypothesis_id]
            session.steps.append(DiagnosticStep(
                experiment_id=experiment.experiment_id,
                expected_information_gain_bits=information_gain,
                utility=utility,
                observed_outcome=outcome,
                evidence_ref=evidence_record.evidence_id,
                posterior=posterior,
            ))
            completed.add(experiment.experiment_id)
        winner = max(session.hypotheses, key=lambda item: item.probability)
        if winner.probability >= confidence_threshold:
            winner.status = "confirmed_candidate"
            session.status = "root_cause_candidate"
            return session
        session.status = "blocked_step_limit"
        return session


def expected_information_gain(prior: dict[str, float], experiment: CandidateExperiment) -> float:
    prior_entropy = entropy(prior.values())
    expected_posterior_entropy = 0.0
    for outcome in experiment.outcomes:
        outcome_probability = sum(
            prior[hypothesis_id] * experiment.likelihoods[hypothesis_id].get(outcome, 0.0)
            for hypothesis_id in prior
        )
        if outcome_probability <= 0:
            continue
        posterior = {
            hypothesis_id: prior[hypothesis_id]
            * experiment.likelihoods[hypothesis_id].get(outcome, 0.0)
            / outcome_probability
            for hypothesis_id in prior
        }
        expected_posterior_entropy += outcome_probability * entropy(posterior.values())
    return max(0.0, prior_entropy - expected_posterior_entropy)


def bayesian_update(
    prior: dict[str, float], experiment: CandidateExperiment, observed_outcome: str
) -> dict[str, float]:
    weighted = {
        hypothesis_id: probability
        * experiment.likelihoods[hypothesis_id].get(observed_outcome, 0.0)
        for hypothesis_id, probability in prior.items()
    }
    return _normalized(weighted)


def entropy(probabilities) -> float:
    return -sum(value * math.log2(value) for value in probabilities if value > 0)


def seeded_excess_current_session(session_id: str = "seeded-current-001") -> DiagnosticSession:
    hypotheses = [
        Hypothesis("H_LEAK", "PCB or load leakage remains when firmware is held reset", 1 / 3),
        Hypothesis("H_FW", "Firmware leaves a peripheral or radio subsystem awake", 1 / 3),
        Hypothesis("H_REG", "Regulator quiescent-current or assembly variant regression", 1 / 3),
    ]
    experiments = [
        CandidateExperiment(
            "E_RESET", "Does excess current disappear while MCU reset is asserted?",
            ["drops", "stays"],
            {
                "H_LEAK": {"drops": 0.05, "stays": 0.95},
                "H_FW": {"drops": 0.98, "stays": 0.02},
                "H_REG": {"drops": 0.03, "stays": 0.97},
            },
            time_cost=1.0, risk_cost=0.05,
        ),
        CandidateExperiment(
            "E_ISOLATE_LOAD", "Does disconnecting the suspect load remove excess current?",
            ["drops", "stays"],
            {
                "H_LEAK": {"drops": 0.85, "stays": 0.15},
                "H_FW": {"drops": 0.55, "stays": 0.45},
                "H_REG": {"drops": 0.05, "stays": 0.95},
            },
            time_cost=2.0, risk_cost=0.2,
        ),
        CandidateExperiment(
            "E_REGULATOR_AB", "Does substituting a golden regulator path remove excess current?",
            ["drops", "stays"],
            {
                "H_LEAK": {"drops": 0.05, "stays": 0.95},
                "H_FW": {"drops": 0.05, "stays": 0.95},
                "H_REG": {"drops": 0.98, "stays": 0.02},
            },
            time_cost=5.0, risk_cost=0.5, monetary_cost=0.3,
        ),
    ]
    return DiagnosticSession(session_id, hypotheses, experiments)


def simulated_excess_current_observer(true_hypothesis: str):
    outcomes = {
        "H_LEAK": {"E_RESET": "stays", "E_ISOLATE_LOAD": "drops", "E_REGULATOR_AB": "stays"},
        "H_FW": {"E_RESET": "drops", "E_ISOLATE_LOAD": "drops", "E_REGULATOR_AB": "stays"},
        "H_REG": {"E_RESET": "stays", "E_ISOLATE_LOAD": "stays", "E_REGULATOR_AB": "drops"},
    }
    if true_hypothesis not in outcomes:
        raise ValueError(f"unknown seeded hypothesis: {true_hypothesis}")

    def observe(experiment: CandidateExperiment) -> tuple[str, dict[str, Any]]:
        outcome = outcomes[true_hypothesis][experiment.experiment_id]
        current_ma = 1.2 if outcome == "drops" else 5.2
        return outcome, {
            "current_ma": current_ma,
            "uncertainty_ma": 0.05,
            "configuration": {"board_revision": "SIM-A", "firmware_revision": "simulated"},
        }

    return observe


def _normalized(values: dict[str, float]) -> dict[str, float]:
    if any(not math.isfinite(value) or value < 0 for value in values.values()):
        raise ValueError("probabilities must be finite and non-negative")
    total = sum(values.values())
    if total <= 0:
        raise ValueError("probability mass collapsed to zero")
    return {key: value / total for key, value in values.items()}


def _validate_session(session: DiagnosticSession) -> None:
    ids = {item.hypothesis_id for item in session.hypotheses}
    if not ids or len(ids) != len(session.hypotheses):
        raise ValueError("hypothesis IDs must be non-empty and unique")
    _normalized(session.probabilities())
    experiment_ids: set[str] = set()
    for experiment in session.experiments:
        if experiment.experiment_id in experiment_ids:
            raise ValueError("experiment IDs must be unique")
        experiment_ids.add(experiment.experiment_id)
        if set(experiment.likelihoods) != ids:
            raise ValueError("every experiment needs a likelihood model for every hypothesis")
        for hypothesis_id, likelihoods in experiment.likelihoods.items():
            total = sum(likelihoods.get(outcome, 0.0) for outcome in experiment.outcomes)
            if not math.isclose(total, 1.0, rel_tol=1e-6, abs_tol=1e-6):
                raise ValueError(f"likelihoods for {hypothesis_id} do not sum to one")
