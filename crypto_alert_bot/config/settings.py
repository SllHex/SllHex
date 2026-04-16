"""Application settings loaded from environment."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

_admin_ids_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: list[int] = [
    int(item.strip()) for item in _admin_ids_raw.split(",") if item.strip().isdigit()
]

COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"
CHECK_INTERVAL_SECONDS: int = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))
DB_PATH: str = os.getenv("DB_PATH", "data/alerts.db")
MAX_ALERTS_PER_USER: int = int(os.getenv("MAX_ALERTS_PER_USER", "5"))
