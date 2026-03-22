import subprocess
import time
import pytest
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

@pytest.fixture(scope="session")
def django_server():
    """Start Django dev server for Playwright tests."""
    proc = subprocess.Popen(
        ["venv/bin/python", "manage.py", "runserver", "8765", "--noreload"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    yield "http://127.0.0.1:8765"
    proc.terminate()
    proc.wait()
