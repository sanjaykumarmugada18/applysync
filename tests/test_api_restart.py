"""Real HTTP and process restart, never PostgreSQL service restart."""

from contextlib import contextmanager
from pathlib import Path
import socket
import subprocess
import sys
import time
from uuid import uuid4

import httpx
import pytest
from sqlalchemy import delete

from database import session_scope
from models import JobApplication

pytestmark = pytest.mark.database


@contextmanager
def test_server():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    code = ("import uvicorn; from main import create_app; "
            "app=create_app('test'); assert app.state.database_target == 'test'; "
            f"uvicorn.run(app, host='127.0.0.1', port={port}, access_log=False)")
    process = subprocess.Popen(
        [sys.executable, "-c", code], cwd=Path(__file__).resolve().parents[1],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", trust_env=False, timeout=5) as client:
            deadline = time.monotonic() + 15
            while True:
                assert process.poll() is None, "Test Uvicorn process exited during startup"
                try:
                    health = client.get("/health")
                    break
                except httpx.TransportError:
                    if time.monotonic() >= deadline:
                        pytest.fail("Test Uvicorn startup timed out")
                    time.sleep(0.1)
            assert health.status_code == 200 and health.json() == {"status": "healthy"}
            missing = client.get("/unknown")
            assert missing.status_code == 404 and missing.json() == {"detail": "Not Found"}
            yield client, process
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


# This context manager is a helper, not a collected test.
test_server.__test__ = False


def test_committed_application_survives_uvicorn_restart(test_engine):
    # test_engine verifies current database, current role and revision before spawning.
    company = f"Synthetic restart {uuid4()}"
    try:
        with test_server() as (client, first_process):
            response = client.post("/applications", json={
                "company": company, "role": "Engineer", "applied_on": "2026-09-17"})
            assert response.status_code == 201
            stored = response.json()
        assert first_process.poll() is not None
        with test_server() as (client, second_process):
            assert first_process.pid != second_process.pid
            response = client.get(f'/applications/{stored["id"]}')
            assert response.status_code == 200
            assert response.json() == stored
    finally:
        # A unique synthetic company also covers a response lost after commit.
        with session_scope(test_engine) as session:
            session.execute(delete(JobApplication).where(JobApplication.company == company))
