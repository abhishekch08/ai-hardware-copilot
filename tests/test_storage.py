import tempfile
import unittest

from ai_hardware_copilot.conference import ConferenceEngine
from ai_hardware_copilot.models import ConferenceState
from ai_hardware_copilot.provider import ScriptedProvider
from ai_hardware_copilot.storage import ConferenceStore

from .common import directory, product_task, routing


class StorageTests(unittest.TestCase):
    def test_saved_record_round_trips(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = ConferenceStore(temporary)
            agent_directory = directory()
            engine = ConferenceEngine(
                agent_directory,
                routing(agent_directory),
                ScriptedProvider(),
                store,
            )
            original = engine.run_initial(product_task())
            restored = store.load(original.conference_id)
            self.assertEqual(restored.state, ConferenceState.OBJECTIONS_RESOLVED)
            self.assertEqual(len(restored.attendance), 184)
            self.assertEqual(len(restored.active_agents), len(original.active_agents))
            self.assertEqual(restored.task.metadata["context_sha256"], original.task.metadata["context_sha256"])


if __name__ == "__main__":
    unittest.main()

