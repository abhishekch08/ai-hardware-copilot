import unittest

from ai_hardware_copilot.schema_validation import SchemaValidationError, validate_json


class SchemaValidationTests(unittest.TestCase):
    def test_required_type_enum_and_additional_properties(self):
        schema = {
            "type": "object",
            "required": ["verdict", "confidence"],
            "properties": {
                "verdict": {"enum": ["approve", "object"]},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            },
            "additionalProperties": False,
        }
        validate_json({"verdict": "approve", "confidence": 0.8}, schema)
        with self.assertRaises(SchemaValidationError):
            validate_json({"verdict": "guess", "confidence": 0.8}, schema)
        with self.assertRaises(SchemaValidationError):
            validate_json({"verdict": "approve", "confidence": 2}, schema)
        with self.assertRaises(SchemaValidationError):
            validate_json({"verdict": "approve", "confidence": 0.8, "extra": True}, schema)


if __name__ == "__main__":
    unittest.main()
