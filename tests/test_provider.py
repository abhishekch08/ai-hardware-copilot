import unittest

from ai_hardware_copilot.models import AttendanceRecord, Relevance
from ai_hardware_copilot.provider import HttpJsonProvider

from .common import ROOT, directory, product_task


class StubHttpProvider(HttpJsonProvider):
    def __init__(self, response):
        super().__init__("http://localhost:9999", repo_root=ROOT)
        self.response = response

    def _post(self, operation, payload):
        return dict(self.response)


class ProviderTests(unittest.TestCase):
    def test_model_cannot_demote_deterministic_relevance(self):
        provider = StubHttpProvider({"relevance": "out_of_scope", "score": 0})
        deterministic = AttendanceRecord(
            agent_id="EE-02",
            proposal_version=1,
            relevance=Relevance.PRIMARY,
            score=10,
            mandatory=False,
            reasons=["power domain"],
        )
        result = provider.assess_relevance(
            directory().get("EE-02"), product_task(), deterministic
        )
        self.assertEqual(result.relevance, Relevance.PRIMARY)
        self.assertEqual(result.score, 10)

    def test_active_agent_payload_embeds_hashed_canonical_handbook(self):
        provider = StubHttpProvider({})
        payload = provider._agent_payload(directory().get("EE-02"), include_documents=True)
        documents = {item["path"]: item for item in payload["instruction_documents"]}
        handbook = "agents/02_ELECTRICAL_ELECTRONICS.md"
        self.assertIn(handbook, documents)
        self.assertEqual(len(documents[handbook]["sha256"]), 64)
        self.assertIn("Power Electronics", documents[handbook]["content"])


if __name__ == "__main__":
    unittest.main()
