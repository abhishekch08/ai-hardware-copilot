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

    def test_local_ui_and_plain_language_conference_flow(self):
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
                connection = http.client.HTTPConnection(
                    "127.0.0.1", server.server_address[1], timeout=10
                )
                connection.request("GET", "/")
                response = connection.getresponse()
                self.assertEqual(response.status, 200)
                self.assertIn("default-src 'self'", response.getheader("Content-Security-Policy"))
                self.assertIn(b"Start an engineering conference", response.read())

                connection.request(
                    "GET", "/v1/config", headers={"Authorization": "Bearer test-token"}
                )
                response = connection.getresponse()
                config = json.loads(response.read())
                self.assertEqual(config["agents"], 184)
                self.assertFalse(config["reasoning_enabled"])

                body = json.dumps({
                    "operation": "idea_conference",
                    "payload": {
                        "task_id": "web-ui-test-001",
                        "title": "Wearable concept",
                        "idea": (
                            "Design a compact wearable with optical sensing, Bluetooth, "
                            "a rechargeable battery and a manufacturable enclosure."
                        ),
                        "risk_tier": "T2",
                        "iterate_rounds": 0,
                    },
                })
                connection.request(
                    "POST", "/v1/jobs", body,
                    {
                        "Authorization": "Bearer test-token",
                        "Content-Type": "application/json",
                        "Idempotency-Key": "ui-test-001",
                    },
                )
                response = connection.getresponse()
                self.assertEqual(response.status, 202)
                job_id = json.loads(response.read())["job_id"]
                deadline = time.monotonic() + 8
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
                        self.fail("idea conference did not finish")
                    time.sleep(0.02)
                self.assertEqual(job["status"], "succeeded", job.get("error"))
                conference_id = job["result"]["conference_id"]

                connection.request(
                    "GET", f"/v1/conferences/{conference_id}",
                    headers={"Authorization": "Bearer test-token"},
                )
                response = connection.getresponse()
                view = json.loads(response.read())
                self.assertEqual(view["agents_screened"], 184)
                self.assertEqual(view["task"]["title"], "Wearable concept")
                self.assertEqual(view["provider"], "dry-run")
                self.assertTrue(view["positions"])
                self.assertIn("Engineering Conference", view["report_markdown"])

                connection.request(
                    "GET", "/v1/jobs?limit=10",
                    headers={"Authorization": "Bearer test-token"},
                )
                response = connection.getresponse()
                jobs = json.loads(response.read())["jobs"]
                self.assertEqual(jobs[0]["conference_id"], conference_id)
            finally:
                if connection:
                    connection.close()
                server.shutdown()
                server.server_close()
                worker.stop()
                thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
