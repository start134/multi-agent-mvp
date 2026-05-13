from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Multi Agent Automation MVP")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/agent_mvp.db")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY") or None
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

settings = Settings()
