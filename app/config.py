from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

REQUIRED_ENV_VARS = [
    "WHATSAPP_ACCESS_TOKEN",
    "WHATSAPP_PHONE_NUMBER_ID",
    "WHATSAPP_VERIFY_TOKEN",
    "META_APP_SECRET",
    "OPENROUTER_API_KEY",
    "DATABASE_URL",
]

def validate_environment():
    missing = [
        variable
        for variable in REQUIRED_ENV_VARS
        if not os.getenv(variable)
    ]

    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
    