import os

from dotenv import load_dotenv

DOTENV_PATHS = {
    "development": ".env.development",
    "test": ".env.test",
    "production": ".env.production",
}


def load_env_vars():
    """Load environment variables from .env file based on PYTHON_ENV."""

    python_env = os.environ["PYTHON_ENV"]
    load_dotenv(dotenv_path=DOTENV_PATHS[python_env])

    return python_env
