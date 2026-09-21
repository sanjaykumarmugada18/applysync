"""Start a real Uvicorn child process and check loopback HTTP, then stop it."""

from pathlib import Path
import socket
import subprocess
import sys
import time

import httpx


def main():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1",
         "--port", str(port), "--no-access-log"],
        cwd=Path(__file__).resolve().parents[1],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", trust_env=False, timeout=1) as client:
            deadline = time.monotonic() + 15
            while True:
                if process.poll() is not None:
                    raise RuntimeError("Uvicorn exited before the HTTP checks completed.")
                try:
                    health = client.get("/health")
                    break
                except httpx.TransportError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError("Uvicorn did not become reachable in time.") from None
                    time.sleep(0.1)
            assert health.status_code == 200
            assert health.json() == {"status": "healthy"}
            missing = client.get("/does-not-exist")
            assert missing.status_code == 404
            assert missing.json() == {"detail": "Not Found"}
            assert process.poll() is None
            print('Actual Uvicorn HTTP: /health -> 200 {"status":"healthy"}')
            print('Actual Uvicorn HTTP: /does-not-exist -> 404 {"detail":"Not Found"}')
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        print("Smoke-check child process stopped; no existing server was stopped.")


if __name__ == "__main__":
    main()
