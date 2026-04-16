"""Alert creation and management handlers."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config.settings import MAX_ALERTS_PER_USER
from database.db import add_alert, count_user_alerts, delete_alert, get_user_alerts
from keyboards.inline import (
    coin_selection_keyboard,
    confirm_alert_keyboard,
    delete_confirm_keyboard,
    delete_alert_keyboard,
    direction_keyboard,
)
from services.crypto_api import get_price, search_coin
from utils.formatters import format_alert_list, format_price
from utils.validators import validate_price

router = Router()


class AlertStates(StatesGroup):
    waiting_for_coin = State()
    waiting_for_price = State()
    waiting_for_direction = State()
    confirm = State()


@router.message(Command("add_alert"))
@router.message(F.text == "➕ Add Alert")
async def add_alert_start(message: Message, state: FSMContext) -> None:
    total = await count_user_alerts(message.from_user.id)
    if total >= MAX_ALERTS_PER_USER:
        await message.answer(
            f"You already have {MAX_ALERTS_PER_USER} active alerts. Upgrade required for more."
        )
        return

    await state.clear()
    await state.set_state(AlertStates.waiting_for_coin)
    await message.answer("Type a coin name or symbol (example: bitcoin or btc).")


@router.message(AlertStates.waiting_for_coin)
async def receive_coin(message: Message, state: FSMContext) -> None:
    coins = await search_coin(message.text.strip())
    if not coins:
        await message.answer("No coins found. Try again with another query.")
        return

    await state.update_data(coins=coins)
    await message.answer(
        "Select a coin:",
        reply_markup=coin_selection_keyboard(coins),
    )


@router.callback_query(F.data.startswith("select_coin:"))
async def select_coin(callback: CallbackQuery, state: FSMContext) -> None:
    _, coin_id, symbol = callback.data.split(":", maxsplit=2)
    await state.update_data(coin_id=coin_id, coin_symbol=symbol.upper())
    await state.set_state(AlertStates.waiting_for_price)
    await callback.message.answer("Now enter your target price in USD.")
    await callback.answer()


@router.message(AlertStates.waiting_for_price)
async def receive_price(message: Message, state: FSMContext) -> None:
    value = validate_price(message.text)
    if value is None:
        await message.answer("Invalid price. Enter a positive number like 45000 or 0.005.")
        return

    await state.update_data(target_price=value)
    await state.set_state(AlertStates.waiting_for_direction)
    await message.answer("Choose alert direction:", reply_markup=direction_keyboard())


@router.callback_query(F.data.startswith("dir:"))
async def select_direction(callback: CallbackQuery, state: FSMContext) -> None:
    direction = callback.data.split(":", maxsplit=1)[1]
    await state.update_data(direction=direction)
    data = await state.get_data()
    await state.set_state(AlertStates.confirm)

    text = (
        "Please confirm your alert:\n\n"
        f"• Coin: {data['coin_symbol']} ({data['coin_id']})\n"
        f"• Target: {format_price(float(data['target_price']))}\n"
        f"• Direction: {direction.upper()}"
    )
    await callback.message.answer(text, reply_markup=confirm_alert_keyboard())
    await callback.answer()


@router.callback_query(F.data == "confirm_alert")
async def confirm_alert(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    alert_id = await add_alert(
        user_id=callback.from_user.id,
        coin_id=data["coin_id"],
        coin_symbol=data["coin_symbol"],
        target_price=float(data["target_price"]),
        direction=data["direction"],
    )
    await state.clear()
    await callback.message.answer(f"✅ Alert created successfully. ID: {alert_id}")
    await callback.answer()


@router.callback_query(F.data == "cancel_alert")
async def cancel_alert(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("Alert creation canceled.")
    await callback.answer()


@router.message(Command("my_alerts"))
@router.message(F.text == "⚠️ My Alerts")
async def my_alerts(message: Message) -> None:
    alerts = await get_user_alerts(message.from_user.id)
    prices: dict[str, float] = {}
    for alert in alerts:
        if alert["coin_id"] not in prices:
            fetched = await get_price(alert["coin_id"])
            if fetched is not None:
                prices[alert["coin_id"]] = fetched

    text = format_alert_list(alerts, prices)
    await message.answer(text, parse_mode="HTML")
    for alert in alerts:
        await message.answer(
            f"Manage alert #{alert['id']} ({alert['coin_symbol']})",
            reply_markup=delete_alert_keyboard(alert["id"]),
        )


@router.callback_query(F.data.startswith("delete:"))
async def request_delete(callback: CallbackQuery) -> None:
    alert_id = int(callback.data.split(":", maxsplit=1)[1])
    await callback.message.answer(
        f"Delete alert #{alert_id}?", reply_markup=delete_confirm_keyboard(alert_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_yes:"))
async def confirm_delete(callback: CallbackQuery) -> None:
    alert_id = int(callback.data.split(":", maxsplit=1)[1])
    ok = await delete_alert(alert_id=alert_id, user_id=callback.from_user.id)
    await callback.message.answer("Deleted." if ok else "Alert not found.")
    await callback.answer()


@router.callback_query(F.data == "delete_no")
@router.callback_query(F.data == "back")
async def cancel_delete(callback: CallbackQuery) -> None:
    await callback.answer("Canceled")


@router.callback_query(F.data == "add_alert")
async def add_alert_from_button(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await add_alert_start(callback.message, state)
