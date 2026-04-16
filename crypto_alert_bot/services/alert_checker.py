"""Background service for checking and triggering alerts."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot

from config.settings import CHECK_INTERVAL_SECONDS
from database.db import deactivate_alert, get_all_active_alerts
from services.crypto_api import get_price
from services.notifier import send_alert_notification

logger = logging.getLogger(__name__)


async def check_alerts(bot: Bot) -> None:
    alerts = await get_all_active_alerts()
    if not alerts:
        return

    alerts_by_coin: dict[str, list[dict]] = {}
    for alert in alerts:
        alerts_by_coin.setdefault(alert["coin_id"], []).append(alert)

    prices: dict[str, float] = {}
    for coin_id in alerts_by_coin:
        price = await get_price(coin_id)
        if price is not None:
            prices[coin_id] = price

    for coin_id, coin_alerts in alerts_by_coin.items():
        current_price = prices.get(coin_id)
        if current_price is None:
            continue

        for alert in coin_alerts:
            direction = alert["direction"]
            target_price = float(alert["target_price"])
            triggered = (direction == "above" and current_price >= target_price) or (
                direction == "below" and current_price <= target_price
            )
            if not triggered:
                continue

            try:
                await send_alert_notification(
                    bot=bot,
                    user_id=alert["user_id"],
                    coin_symbol=alert["coin_symbol"],
                    target_price=target_price,
                    current_price=current_price,
                    direction=direction,
                )
                await deactivate_alert(alert["id"])
            except Exception:
                logger.exception("Failed to notify user for alert_id=%s", alert["id"])


async def start_checker(bot: Bot) -> None:
    while True:
        try:
            await check_alerts(bot)
        except Exception:
            logger.exception("Unexpected error in checker loop")
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)
