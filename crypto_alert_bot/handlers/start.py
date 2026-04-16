"""Start and utility user handlers."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.reply import main_menu_keyboard
from services.crypto_api import get_price, get_top_coins
from utils.formatters import format_percentage, format_price

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    btc = await get_price("bitcoin")
    eth = await get_price("ethereum")
    bnb = await get_price("binancecoin")

    price_lines = [
        f"• BTC: {format_price(btc)}" if btc is not None else "• BTC: unavailable",
        f"• ETH: {format_price(eth)}" if eth is not None else "• ETH: unavailable",
        f"• BNB: {format_price(bnb)}" if bnb is not None else "• BNB: unavailable",
    ]

    prices_block = "\n".join(price_lines)
    text = (
        "👋 <b>Welcome to Crypto Price Alert Bot</b>\n\n"
        "Set smart crypto alerts and get notified the moment price moves above or below your target.\n\n"
        "<b>Live Prices</b>\n"
        f"{prices_block}"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu_keyboard())


@router.message(F.text == "📊 Top Coins")
async def top_coins_handler(message: Message) -> None:
    coins = await get_top_coins(limit=10)
    if not coins:
        await message.answer("Could not fetch top coins right now.")
        return

    lines = ["📊 <b>Top Coins by Market Cap</b>"]
    for coin in coins:
        price = coin.get("current_price")
        pct = coin.get("price_change_percentage_24h")
        lines.append(
            f"• {coin['name']} ({coin['symbol']}) — {format_price(float(price)) if isinstance(price, (int, float)) else 'N/A'}"
            f" | {format_percentage(float(pct)) if isinstance(pct, (int, float)) else 'N/A'}"
        )

    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(F.text == "ℹ️ Help")
async def help_handler(message: Message) -> None:
    await message.answer(
        "Use /add_alert to create a price alert, /my_alerts to manage alerts, and wait for automatic notifications."
    )
