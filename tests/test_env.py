import os

from app.env import load_env_vars


# Be confident tests are loading the correct env vars
def test_load_env_vars():
    python_env = load_env_vars()
    assert python_env == "test"
    assert os.environ.get("PYTHON_ENV") == "test"
    assert os.environ.get("PGDATABASE") == "demo_fastapi_test"
