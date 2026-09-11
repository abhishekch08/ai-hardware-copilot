import tempfile
import time
import unittest
from pathlib import Path

from ai_hardware_copilot.jobs import JobQueue, JobWorker


class JobQueueTests(unittest.TestCase):
    def test_idempotency_and_worker_persist_result(self):
        with tempfile.TemporaryDirectory() as temporary:
            queue = JobQueue(Path(temporary) / "jobs.sqlite3")
            first = queue.enqueue("echo", {"value": 42}, "same-request")
            second = queue.enqueue("echo", {"value": 42}, "same-request")
            self.assertEqual(first.job_id, second.job_id)
            worker = JobWorker(queue, lambda operation, payload: {
                "operation": operation, "value": payload["value"]
            })
            worker.start()
            deadline = time.monotonic() + 3
            while queue.get(first.job_id).status not in {"succeeded", "failed"}:
                if time.monotonic() > deadline:
                    self.fail("job did not finish")
                time.sleep(0.01)
            worker.stop()
            completed = queue.get(first.job_id)
            self.assertEqual(completed.status, "succeeded")
            self.assertEqual(completed.result["value"], 42)

    def test_idempotency_key_reuse_with_different_payload_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            queue = JobQueue(Path(temporary) / "jobs.sqlite3")
            queue.enqueue("echo", {"value": 42}, "same-request")
            with self.assertRaises(ValueError):
                queue.enqueue("echo", {"value": 999}, "same-request")

    def test_interrupted_running_job_is_requeued_on_restart(self):
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "jobs.sqlite3"
            queue = JobQueue(database)
            queued = queue.enqueue("echo", {})
            claimed = queue.claim_next()
            self.assertEqual(claimed.job_id, queued.job_id)
            self.assertEqual(claimed.status, "running")
            restarted = JobQueue(database)
            self.assertEqual(restarted.get(queued.job_id).status, "queued")


if __name__ == "__main__":
    unittest.main()
