"""Admin-only handlers."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.settings import ADMIN_IDS
from database.db import get_admin_stats, get_all_unique_users

router = Router()


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return

    stats = await get_admin_stats()
    top = stats["top_coins"]
    top_text = ", ".join(f"{item['coin_symbol']} ({item['cnt']})" for item in top) or "N/A"

    text = (
        "📈 <b>Bot Stats</b>\n"
        f"• Total users: {stats['total_users']}\n"
        f"• Total active alerts: {stats['total_active_alerts']}\n"
        f"• Most tracked coins: {top_text}"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("broadcast"))
async def broadcast_handler(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /broadcast <message>")
        return

    body = parts[1].strip()
    users = await get_all_unique_users()

    sent = 0
    failed = 0
    for user_id in users:
        try:
            await message.bot.send_message(user_id, body)
            sent += 1
        except Exception:
            failed += 1

    await message.answer(f"Broadcast done. Sent: {sent}, Failed: {failed}")
