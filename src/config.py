from pathlib import Path
import os
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
API_KEY = os.getenv("GROQ_API_KEY", "").strip()
DATA_DIR = Path(os.getenv("APP_DATA_DIR", ROOT_DIR / "data"))


def get_client():
    """Return a Groq client or raise a readable configuration error."""
    key = os.getenv("GROQ_API_KEY", API_KEY).strip()
    if not key:
        raise RuntimeError(
            "Groq API key is missing. Open the project .env file, set GROQ_API_KEY, "
            "save it, and restart the application."
        )
    try:
        from groq import Groq
    except ImportError as exc:
        raise RuntimeError("Groq package is missing. Run: python -m pip install -r requirements.txt") from exc
    return Groq(api_key=key)
