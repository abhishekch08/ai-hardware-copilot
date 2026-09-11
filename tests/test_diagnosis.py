import json
import tempfile
import unittest
from dataclasses import asdict

from ai_hardware_copilot.diagnosis import (
    DiagnosticEngine,
    seeded_excess_current_session,
    simulated_excess_current_observer,
)
from ai_hardware_copilot.evidence import EvidenceStore
from ai_hardware_copilot.schema_validation import validate_json

from .common import ROOT


class DiagnosisTests(unittest.TestCase):
    def test_seeded_faults_converge_from_evidence_not_checklist_order(self):
        for true_hypothesis in ("H_LEAK", "H_FW", "H_REG"):
            with self.subTest(true_hypothesis=true_hypothesis), tempfile.TemporaryDirectory() as temporary:
                session = seeded_excess_current_session(f"session-{true_hypothesis}")
                result = DiagnosticEngine(EvidenceStore(temporary)).run(
                    session,
                    simulated_excess_current_observer(true_hypothesis),
                    confidence_threshold=0.9,
                    max_steps=3,
                )
                winner = max(result.hypotheses, key=lambda item: item.probability)
                self.assertEqual(winner.hypothesis_id, true_hypothesis)
                self.assertGreaterEqual(winner.probability, 0.9)
                self.assertEqual(result.status, "root_cause_candidate")
                self.assertTrue(result.steps)
                schema = json.loads(
                    (ROOT / "schemas/runtime/diagnostic-session.schema.json").read_text(
                        encoding="utf-8"
                    )
                )
                validate_json(asdict(result), schema)


if __name__ == "__main__":
    unittest.main()
