"""Guarded browser -> FastAPI -> test PostgreSQL checks; no dev writes or DDL."""

from datetime import datetime, timezone
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from uuid import uuid4

import httpx
from sqlalchemy import delete, func, select, text

from config import load_settings
from database import build_engine, session_scope
from models import JobApplication

ROOT = Path(__file__).resolve().parents[1]
PHASE = "configuration"


def verify_target(engine):
    with engine.connect() as connection:
        if (connection.scalar(text("SELECT current_database()")) != "applysync_test"
                or connection.scalar(text("SELECT current_user")) != "applysync_test"
                or connection.scalar(text("SELECT version_num FROM alembic_version")) != "0001"):
            raise RuntimeError("Refusing an unverified integration database target.")


def serve(port):
    import uvicorn
    from main import create_app
    engine = build_engine(load_settings("test"))
    verify_target(engine)
    app = create_app("test")
    app.state.engine = engine
    uvicorn.run(app, host="127.0.0.1", port=port, access_log=False)


def run():
    global PHASE
    engine = build_engine(load_settings("test"))
    process = None
    marker = f"Synthetic Browser {uuid4()}"
    verified = False
    try:
        verify_target(engine)
        verified = True
        PHASE = "test fixture creation"
        # Enough owned fixtures to exercise real pagination, even in a nonempty DB.
        with session_scope(engine) as session:
            for i in range(21):
                session.add(JobApplication(company=f"{marker} seed {i:02}", role="Engineer",
                    applied_on=datetime(2026, 9, 1).date(),
                    created_at=datetime(1900, 1, 1, tzinfo=timezone.utc)))
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        origin = f"http://127.0.0.1:{port}"
        PHASE = "isolated API startup"
        print("Verified test target; starting isolated API.", flush=True)
        process = subprocess.Popen([sys.executable, "-c",
            f"from scripts.run_frontend_integration import serve; serve({port})"],
            cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        with httpx.Client(trust_env=False, timeout=2) as client:
            deadline = time.monotonic() + 20
            while True:
                if process.poll() is not None:
                    raise RuntimeError("Isolated test API did not start.")
                try:
                    response = client.get(origin + "/health")
                    if response.status_code == 200:
                        break
                except httpx.TransportError:
                    pass
                if time.monotonic() > deadline:
                    raise RuntimeError("Isolated test API startup timed out.")
                time.sleep(.1)
        env = {**os.environ, "APPLYSYNC_E2E_RUN_ID": marker,
               "APPLYSYNC_E2E_API_ORIGIN": origin, "VITE_API_BASE_URL": origin}
        command = ["cmd.exe", "/d", "/c", "npm.cmd", "run", "test:integration"] if os.name == "nt" else ["npm", "run", "test:integration"]
        PHASE = "browser checks"
        print("Isolated API healthy; running browser checks.", flush=True)
        result = subprocess.run(command, cwd=ROOT / "frontend", env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        print(result.stdout, flush=True)
        if result.returncode:
            raise RuntimeError("Browser integration checks failed; see test output.")
        PHASE = "committed record verification"
        with session_scope(engine) as session:
            row = session.scalar(select(JobApplication).where(JobApplication.company == marker + " created"))
            if row is None or row.role != "Browser Engineer" or row.applied_on.isoformat() != "2100-01-01":
                raise RuntimeError("Committed browser record was not verified in PostgreSQL.")
        print("PASS: committed browser-created values independently verified in test PostgreSQL.")
    finally:
        if process is not None:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        try:
            if verified:
                verify_target(engine)  # Recheck before any cleanup.
                with session_scope(engine) as session:
                    session.execute(delete(JobApplication).where(JobApplication.company.startswith(marker)))
                with session_scope(engine) as session:
                    remaining = session.scalar(select(func.count()).select_from(JobApplication).where(JobApplication.company.startswith(marker)))
                    if remaining != 0:
                        raise RuntimeError("Owned fixture cleanup was incomplete.")
                print("PASS: only this run's uniquely marked test records cleaned up; target reverified.")
        finally:
            engine.dispose()


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        # Never expose raw configuration, connection URLs or database exceptions.
        print(f"Integration verification failed during {PHASE} ({type(error).__name__}, OS code {getattr(error, 'winerror', None)}). Check dedicated test setup and test results; private details suppressed.")
        sys.exit(1)
