import json
import tempfile
import unittest
from pathlib import Path

from ai_hardware_copilot.evidence import EvidenceStore


class EvidenceTests(unittest.TestCase):
    def test_registration_is_idempotent_and_tamper_is_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = EvidenceStore(Path(temporary) / "evidence")
            first = store.register_bytes(
                b"measured=1.800 V\n",
                kind="measurement",
                source_uri="instrument://dmm-1/voltage",
                configuration={"board_revision": "A"},
            )
            second = store.register_bytes(
                b"measured=1.800 V\n",
                kind="measurement",
                source_uri="instrument://dmm-1/voltage",
                configuration={"board_revision": "A"},
            )
            self.assertEqual(first.evidence_id, second.evidence_id)
            self.assertTrue(store.verify(first.evidence_id))
            (store.blobs / first.sha256).write_bytes(b"tampered")
            self.assertFalse(store.verify(first.evidence_id))

    def test_record_metadata_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = EvidenceStore(Path(temporary) / "evidence")
            record = store.register_bytes(
                b"measured=1.800 V\n",
                kind="measurement",
                source_uri="instrument://dmm-1/voltage",
                configuration={"board_revision": "A"},
            )
            record_path = store.records / f"{record.evidence_id.rsplit('/', 1)[-1]}.json"
            record_value = json.loads(record_path.read_text(encoding="utf-8"))
            record_value["configuration"]["board_revision"] = "B"
            record_path.write_text(json.dumps(record_value), encoding="utf-8")
            self.assertFalse(store.verify(record.evidence_id))
            with self.assertRaises(ValueError):
                store.register_bytes(
                    b"measured=1.800 V\n",
                    kind="measurement",
                    source_uri="instrument://dmm-1/voltage",
                    configuration={"board_revision": "A"},
                )

    def test_same_bytes_in_different_configuration_get_distinct_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = EvidenceStore(temporary)
            rev_a = store.register_bytes(
                b"42", kind="result", source_uri="test://result",
                configuration={"board_revision": "A"},
            )
            rev_b = store.register_bytes(
                b"42", kind="result", source_uri="test://result",
                configuration={"board_revision": "B"},
            )
            self.assertNotEqual(rev_a.evidence_id, rev_b.evidence_id)
            self.assertEqual(rev_a.sha256, rev_b.sha256)

    def test_claim_assessment_rejects_unknown_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = EvidenceStore(temporary)
            with self.assertRaises(ValueError):
                store.assess_claim(
                    claim_id="C-1", claim="rail is stable", status="supported",
                    evidence_refs=["evidence://sha256/" + "0" * 64],
                    method="review", assessor="TEST-04",
                )


if __name__ == "__main__":
    unittest.main()
