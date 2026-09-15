import unittest

from ai_hardware_copilot.idea import task_from_idea


class IdeaIntakeTests(unittest.TestCase):
    def test_plain_language_idea_becomes_routable_manifest(self):
        task = task_from_idea({
            "task_id": "web-wearable-001",
            "title": "Recovery wearable",
            "idea": (
                "Design a wearable with PPG and IMU sensors, a rechargeable battery, "
                "Bluetooth firmware, a sealed enclosure, mobile app and production test plan."
            ),
            "requirements": "Seven-day battery life\nContinuous skin contact",
            "constraints": ["No display"],
            "iterate_rounds": 3,
        })
        self.assertEqual(task.task_id, "web-wearable-001")
        self.assertIn("electrical", task.domains)
        self.assertIn("embedded", task.domains)
        self.assertIn("mechanical_industrial_wearable", task.domains)
        self.assertIn("power", task.interfaces)
        self.assertIn("firmware", task.interfaces)
        self.assertEqual(task.requirements, ["Seven-day battery life", "Continuous skin contact"])
        self.assertFalse(task.physical_action)

    def test_high_risk_idea_requires_evidence(self):
        with self.assertRaises(ValueError):
            task_from_idea({
                "idea": "Design a medical hardware product with potentially hazardous actuation.",
                "risk_tier": "T3",
            })

    def test_unsafe_task_id_is_rejected(self):
        with self.assertRaises(ValueError):
            task_from_idea({
                "task_id": "../../escape",
                "idea": "Design a bounded sensor product and evaluate its engineering architecture.",
            })

    def test_deliberation_rounds_must_be_a_bounded_integer(self):
        base = {"idea": "Design a bounded sensor product and evaluate its architecture."}
        for value in (True, 2.5, "2.5", -1, 11):
            with self.subTest(value=value), self.assertRaises(ValueError):
                task_from_idea({**base, "iterate_rounds": value})
        task = task_from_idea({**base, "iterate_rounds": "4"})
        self.assertEqual(task.proposal["requested_deliberation_rounds"], 4)


if __name__ == "__main__":
    unittest.main()
