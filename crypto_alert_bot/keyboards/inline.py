"""Inline keyboard builders."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def coin_selection_keyboard(coins: list[dict]) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=f"{coin['name']} ({coin['symbol'].upper()})",
                callback_data=f"select_coin:{coin['id']}:{coin['symbol'].upper()}",
            )
        ]
        for coin in coins
    ]
    rows.append([InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_alert")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def direction_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📈 Price goes ABOVE", callback_data="dir:above")],
            [InlineKeyboardButton(text="📉 Price goes BELOW", callback_data="dir:below")],
        ]
    )


def confirm_alert_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_alert")],
            [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_alert")],
        ]
    )


def delete_alert_keyboard(alert_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Delete Alert", callback_data=f"delete:{alert_id}")],
            [InlineKeyboardButton(text="« Back", callback_data="back")],
        ]
    )


def delete_confirm_keyboard(alert_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Yes, delete", callback_data=f"delete_yes:{alert_id}")],
            [InlineKeyboardButton(text="Cancel", callback_data="delete_no")],
        ]
    )


def new_alert_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Set New Alert", callback_data="add_alert")]
        ]
    )
