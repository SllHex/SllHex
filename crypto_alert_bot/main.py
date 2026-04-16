"""Entry point for crypto alert bot."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Router

from bot.loader import bot, dp
from bot.middlewares.throttle import ThrottleMiddleware
from database.db import init_db
from handlers import admin, alerts, start
from services.alert_checker import start_checker


def register_routers() -> None:
    root_router = Router()
    root_router.include_router(start.router)
    root_router.include_router(alerts.router)
    root_router.include_router(admin.router)
    dp.include_router(root_router)


async def main() -> None:
    register_routers()
    dp.message.middleware(ThrottleMiddleware(period=0.5))
    await init_db()
    asyncio.create_task(start_checker(bot))
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
