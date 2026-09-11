import json
import unittest

from ai_hardware_copilot.gateway import BackendResponse, GatewayEngine


class FakeBackend:
    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []

    def complete(self, *, model, messages):
        self.calls.append((model, messages))
        return BackendResponse(self.outputs.pop(0), model, "request-1", {"tokens": 10})


class GatewayTests(unittest.TestCase):
    def request(self):
        return {
            "operation": "independent_analysis",
            "payload": {
                "agent": {"configuration": {"agent_id": "EE-02"}, "instruction_documents": []},
                "task": {"task_id": "T-1"},
                "model_route": {"profile": "deep"},
                "required_output_schema": {
                    "type": "object",
                    "required": ["agent_id", "proposal_version", "verdict", "confidence", "rationale"],
                    "properties": {
                        "agent_id": {"type": "string"},
                        "proposal_version": {"type": "integer"},
                        "verdict": {"enum": ["approve", "insufficient_evidence"]},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "rationale": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            },
        }

    def test_routes_model_validates_output_and_records_provenance(self):
        output = json.dumps({
            "agent_id": "EE-02", "proposal_version": 1,
            "verdict": "insufficient_evidence", "confidence": 0.2,
            "rationale": "No measured transient was supplied.",
        })
        backend = FakeBackend([output])
        result = GatewayEngine(backend, {"deep": "deep-model"}).handle(self.request())
        self.assertEqual(backend.calls[0][0], "deep-model")
        self.assertEqual(result["_model"]["model"], "deep-model")
        self.assertEqual(len(result["_model"]["prompt_sha256"]), 64)

    def test_invalid_first_output_is_repaired_once(self):
        valid = json.dumps({
            "agent_id": "EE-02", "proposal_version": 1,
            "verdict": "approve", "confidence": 0.9, "rationale": "Verified.",
        })
        backend = FakeBackend(["not-json", valid])
        result = GatewayEngine(backend, {"deep": "deep-model"}, attempts=2).handle(self.request())
        self.assertEqual(result["_model"]["attempt"], 2)
        self.assertEqual(len(backend.calls), 2)


if __name__ == "__main__":
    unittest.main()
