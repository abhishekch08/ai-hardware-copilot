import http.client
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path

from ai_hardware_copilot.jobs import JobQueue, JobWorker
from ai_hardware_copilot.service import ControlPlane, CopilotHttpServer

from .common import ROOT


class ServiceTests(unittest.TestCase):
    def test_authenticated_async_debug_job(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            projects = root / "projects"
            projects.mkdir()
            control = ControlPlane(ROOT, root / "data", projects)
            queue = JobQueue(root / "data" / "jobs.sqlite3")
            worker = JobWorker(queue, control.execute)
            server = CopilotHttpServer(("127.0.0.1", 0), control, queue, "test-token")
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            thread.start()
            connection = None
            try:
                port = server.server_address[1]
                connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
                connection.request("GET", "/health")
                response = connection.getresponse()
                self.assertEqual(response.status, 200)
                self.assertEqual(json.loads(response.read())["agents"], 184)

                body = json.dumps({
                    "operation": "debug_demo",
                    "payload": {"true_hypothesis": "H_FW", "max_steps": 3},
                })
                connection.request(
                    "POST", "/v1/jobs", body,
                    {"Authorization": "Bearer test-token", "Content-Type": "application/json"},
                )
                response = connection.getresponse()
                self.assertEqual(response.status, 202)
                job_id = json.loads(response.read())["job_id"]
                deadline = time.monotonic() + 5
                while True:
                    connection.request(
                        "GET", f"/v1/jobs/{job_id}",
                        headers={"Authorization": "Bearer test-token"},
                    )
                    response = connection.getresponse()
                    job = json.loads(response.read())
                    if job["status"] in {"succeeded", "failed"}:
                        break
                    if time.monotonic() > deadline:
                        self.fail("HTTP job did not finish")
                    time.sleep(0.02)
                self.assertEqual(job["status"], "succeeded", job.get("error"))
                self.assertEqual(job["result"]["status"], "root_cause_candidate")
            finally:
                if connection:
                    connection.close()
                server.shutdown()
                server.server_close()
                worker.stop()
                thread.join(timeout=3)

    def test_jobs_endpoint_rejects_missing_token(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            projects = root / "projects"
            projects.mkdir()
            control = ControlPlane(ROOT, root / "data", projects)
            queue = JobQueue(root / "jobs.sqlite3")
            server = CopilotHttpServer(("127.0.0.1", 0), control, queue, "test-token")
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            connection = None
            try:
                connection = http.client.HTTPConnection(
                    "127.0.0.1", server.server_address[1], timeout=5
                )
                connection.request("POST", "/v1/jobs", "{}", {"Content-Type": "application/json"})
                response = connection.getresponse()
                self.assertEqual(response.status, 401)
                response.read()
            finally:
                if connection:
                    connection.close()
                server.shutdown()
                server.server_close()
                thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
