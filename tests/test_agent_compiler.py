import json
import tempfile
import unittest
from pathlib import Path

from ai_hardware_copilot.directory import AgentDirectory
from scripts.compile_agent_configs import compile_configs

from .common import ROOT


class AgentCompilerTests(unittest.TestCase):
    def test_compiles_registry_and_handbooks_one_to_one(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "agents"
            count = compile_configs(ROOT, output)
            self.assertEqual(count, 184)
            directory = AgentDirectory.from_directory(output)
            self.assertEqual(len(directory), 184)
            self.assertIn("EE-02", directory.ids)
            self.assertIn("XR-01", directory.ids)
            self.assertIn("META-08", directory.ids)

    def test_conference_schemas_are_valid_json(self):
        files = sorted((ROOT / "schemas" / "conference").glob("*.json"))
        self.assertEqual(len(files), 9)
        for path in files:
            with self.subTest(path=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(value["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_runtime_schemas_are_valid_json(self):
        files = sorted((ROOT / "schemas" / "runtime").glob("*.json"))
        self.assertGreaterEqual(len(files), 4)
        for path in files:
            with self.subTest(path=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(value["$schema"], "https://json-schema.org/draft/2020-12/schema")


if __name__ == "__main__":
    unittest.main()
