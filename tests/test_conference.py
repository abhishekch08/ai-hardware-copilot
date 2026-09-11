import tempfile
import unittest

from ai_hardware_copilot.conference import ConferenceEngine
from ai_hardware_copilot.models import ConferenceState
from ai_hardware_copilot.provider import ScriptedProvider
from ai_hardware_copilot.storage import ConferenceStore

from .common import directory, product_task, routing


class ConferenceTests(unittest.TestCase):
    def make_engine(self, temporary, responses=None):
        agent_directory = directory()
        return ConferenceEngine(
            agent_directory,
            routing(agent_directory),
            ScriptedProvider(responses),
            ConferenceStore(temporary),
            max_workers=4,
        )

    def test_clean_conference_can_finalize(self):
        with tempfile.TemporaryDirectory() as temporary:
            engine = self.make_engine(temporary)
            record = engine.run_initial(product_task())
            self.assertEqual(len(record.attendance), 184)
            self.assertEqual(record.state, ConferenceState.OBJECTIONS_RESOLVED)
            report = engine.finalize(record, "Approved scripted architecture fixture.")
            self.assertTrue(report.passed, report.failures)
            self.assertEqual(record.state, ConferenceState.FINALIZED)

    def test_objection_blocks_finalization(self):
        responses = {
            "EE-02": {
                "verdict": "object",
                "rationale": "Peak battery impedance and converter transient are not bounded.",
                "risks": ["Rail brownout during BLE and optical pulse overlap."],
                "conditions": ["Provide corner transient evidence."],
            }
        }
        with tempfile.TemporaryDirectory() as temporary:
            engine = self.make_engine(temporary, responses)
            record = engine.run_initial(product_task())
            self.assertEqual(record.state, ConferenceState.OBJECTIONS_OPEN)
            report = engine.finalize(record, "Must not finalize.")
            self.assertFalse(report.passed)
            self.assertIn("no_objections_open", report.failures)
            self.assertEqual(record.state, ConferenceState.BLOCKED)

    def test_major_objection_requires_evidence_to_resolve(self):
        responses = {"EE-02": {"verdict": "object", "risks": ["Brownout risk"]}}
        with tempfile.TemporaryDirectory() as temporary:
            engine = self.make_engine(temporary, responses)
            record = engine.run_initial(product_task())
            objection = next(item for item in record.objections if item.agent_id == "EE-02")
            with self.assertRaises(ValueError):
                engine.resolve_objection(record, objection.objection_id, "Resolved", "EE-02", [])

    def test_objection_cannot_be_resolved_by_unrelated_agent(self):
        responses = {"EE-02": {"verdict": "object", "risks": ["Brownout risk"]}}
        with tempfile.TemporaryDirectory() as temporary:
            engine = self.make_engine(temporary, responses)
            record = engine.run_initial(product_task())
            objection = next(item for item in record.objections if item.agent_id == "EE-02")
            with self.assertRaises(ValueError):
                engine.resolve_objection(
                    record,
                    objection.objection_id,
                    "Claimed resolution",
                    "META-03",
                    ["evidence/transient.csv"],
                )

    def test_revision_invalidates_old_positions_and_rescreens_every_agent(self):
        with tempfile.TemporaryDirectory() as temporary:
            engine = self.make_engine(temporary)
            record = engine.run_initial(product_task())
            engine.revise_proposal(
                record,
                changes={"power": {"peak_current_margin": "verified"}},
                changed_interfaces=["power", "battery"],
                evidence_refs=["evidence/transient-v2.csv"],
            )
            self.assertEqual(record.task.proposal_version, 2)
            self.assertEqual(len(record.attendance), 184)
            self.assertTrue(all(item.proposal_version == 2 for item in record.attendance.values()))
            report = engine.coverage(record)
            self.assertFalse(report.checks["all_active_reviewed_current_version"])
            engine.collect_independent_positions(record)
            report = engine.coverage(record)
            self.assertTrue(report.checks["all_active_reviewed_current_version"])

    def test_high_risk_approval_without_registered_evidence_fails_closed(self):
        responses = {
            "EE-02": {
                "verdict": "approve",
                "evidence_refs": [],
            }
        }
        with tempfile.TemporaryDirectory() as temporary:
            engine = self.make_engine(temporary, responses)
            record = engine.run_initial(product_task())
            self.assertIn("EE-02", record.analysis_failures)
            report = engine.coverage(record)
            self.assertFalse(report.checks["analysis_provider_healthy"])
            self.assertFalse(report.checks["no_objections_open"])

    def test_deliberation_synthesizes_versioned_revision(self):
        responses = {
            "EE-02": {
                "verdict": "object",
                "risks": ["Unbounded rail transient"],
            },
            "_synthesis": {
                "rationale": "Add an explicit peak-current margin requirement.",
                "proposal_changes": {"power": {"peak_current_margin": "required"}},
                "changed_interfaces": ["power", "battery"],
                "evidence_refs": ["evidence/reference-requirements.md"],
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            engine = self.make_engine(temporary, responses)
            record = engine.run_initial(product_task())
            changed = engine.deliberate_round(record)
            self.assertTrue(changed)
            self.assertEqual(record.task.proposal_version, 2)
            self.assertEqual(len(record.attendance), 184)
            self.assertTrue(record.syntheses)
            self.assertEqual(record.syntheses[-1].round_number, 1)


if __name__ == "__main__":
    unittest.main()
