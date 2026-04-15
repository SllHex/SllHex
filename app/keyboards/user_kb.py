from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Browse Products"), KeyboardButton(text="🧺 My Cart")],
        [KeyboardButton(text="💳 Checkout")],
    ],
    resize_keyboard=True,
)
