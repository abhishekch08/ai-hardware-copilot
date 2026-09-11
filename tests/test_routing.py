import unittest

from ai_hardware_copilot.models import Relevance, TaskManifest

from .common import directory, product_task, routing


class RoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = directory()
        cls.routing = routing(cls.directory)

    def test_every_agent_is_screened(self):
        task = product_task()
        attendance = self.routing.screen_all(task)
        self.assertEqual(len(attendance), 184)
        self.assertEqual(set(attendance), self.directory.ids)
        self.assertTrue(all(item.proposal_version == 1 for item in attendance.values()))

    def test_product_design_and_wearable_dependencies_activate(self):
        attendance = self.routing.screen_all(product_task())
        active = set(self.routing.active_agents(attendance))
        expected = {
            "META-01", "META-04", "META-05", "SYS-01", "SYS-02", "PROD-01",
            "EE-01", "EE-02", "EE-03", "EE-09", "EE-10", "EE-11", "EMB-01",
            "ME-07", "TEST-03", "TEST-09", "AI-13", "REG-03",
        }
        self.assertTrue(expected <= active, sorted(expected - active))

    def test_irrelevant_agent_has_recorded_disposition(self):
        attendance = self.routing.screen_all(product_task())
        record = attendance["XR-02"]
        self.assertIn(record.relevance, set(Relevance))
        self.assertTrue(record.reasons)

    def test_focused_review_screens_everyone_but_activates_a_bounded_cell(self):
        task = TaskManifest.from_dict({
            "task_id": "focused-analog-001",
            "title": "ADC input noise review",
            "objective": "Reduce ADC input-referred noise below 20 microvolts RMS.",
            "description": (
                "Review the op amp anti-alias filter, source impedance, grounding, "
                "acquisition settling and SPICE noise simulation."
            ),
            "task_type": "design_review",
            "risk_tier": "T2",
            "domains": ["electrical"],
            "interfaces": ["analog_front_end"],
            "keywords": ["op amp", "ADC", "noise", "SPICE", "anti alias filter"],
            "requirements": ["input referred noise below 20 microvolts RMS"],
            "constraints": ["do not change the ADC"],
            "proposal": {"circuit": "op amp RC anti alias filter"},
        })
        attendance = self.routing.screen_all(task)
        active = set(self.routing.active_agents(attendance))
        self.assertEqual(len(attendance), 184)
        self.assertLessEqual(len(active), 40)
        self.assertTrue({"EE-01", "EE-11", "EE-14", "TEST-04"} <= active)
        self.assertEqual(attendance["HR-01"].relevance, Relevance.OUT_OF_SCOPE)


if __name__ == "__main__":
    unittest.main()
