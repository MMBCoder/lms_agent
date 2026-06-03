from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

LMS_URL = os.getenv("LMS_URL", "")
LMS_USERNAME = os.getenv("LMS_USERNAME", "")
LMS_PASSWORD = os.getenv("LMS_PASSWORD", "")

HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    str(BASE_DIR / "data" / "lms.db")
)
