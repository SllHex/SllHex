from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.settings import get_settings
from app.db.database import Database
from app.handlers.admin.admin import register_admin_handlers
from app.handlers.common.start import register_start_handlers
from app.handlers.user.store import register_store_handlers
from app.repositories.store_repo import StoreRepository
from app.services.store_service import StoreService


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()

    db = Database()
    db.init()
    db.seed_products()

    repo = StoreRepository(db)
    service = StoreService(repo)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(register_start_handlers(repo))
    dp.include_router(register_store_handlers(repo, service))
    dp.include_router(register_admin_handlers(repo, settings.admin_ids))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
