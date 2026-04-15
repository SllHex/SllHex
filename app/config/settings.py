from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: List[int]



def get_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set. Add it to your environment or .env file.")

    raw_admin_ids = os.getenv("ADMIN_IDS", "")
    admin_ids = [int(value.strip()) for value in raw_admin_ids.split(",") if value.strip().isdigit()]

    return Settings(bot_token=bot_token, admin_ids=admin_ids)
