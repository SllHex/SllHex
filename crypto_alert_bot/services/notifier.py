"""Notification service for triggered alerts."""

from __future__ import annotations

from datetime import datetime, timezone

from aiogram import Bot

from keyboards.inline import new_alert_keyboard
from utils.formatters import format_percentage, format_price


async def send_alert_notification(
    bot: Bot,
    user_id: int,
    coin_symbol: str,
    target_price: float,
    current_price: float,
    direction: str,
) -> None:
    change_pct = ((current_price - target_price) / target_price) * 100 if target_price else 0.0
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    text = (
        "🚨 <b>Alert Triggered!</b>\n\n"
        f"💰 <b>{coin_symbol.upper()}</b> just went <b>{direction}</b> your target!\n\n"
        f"🎯 Your target: <b>{format_price(target_price)}</b>\n"
        f"📈 Current price: <b>{format_price(current_price)}</b> ({format_percentage(change_pct)})\n\n"
        f"⏰ {timestamp}"
    )

    await bot.send_message(
        chat_id=user_id,
        text=text,
        parse_mode="HTML",
        reply_markup=new_alert_keyboard(),
    )
