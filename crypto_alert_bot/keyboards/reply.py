"""Reply keyboards."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Top Coins"), KeyboardButton(text="⚠️ My Alerts")],
            [KeyboardButton(text="➕ Add Alert"), KeyboardButton(text="ℹ️ Help")],
        ],
        resize_keyboard=True,
    )
