import subprocess
import time
import pytest
import os
import sys
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


@pytest.fixture(scope="session")
def django_server():
    """Start Django dev server for Playwright tests."""
    proc = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "8765", "--noreload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__)) or ".",
    )
    
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get("http://127.0.0.1:8765/", timeout=1)
            if response.status_code == 200:
                break
        except:
            time.sleep(0.5)
    else:
        proc.terminate()
        raise RuntimeError("Django server failed to start")
    
    yield "http://127.0.0.1:8765"
    
    proc.terminate()
    proc.wait()


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
