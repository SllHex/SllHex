from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.user_kb import main_menu
from app.repositories.store_repo import StoreRepository

router = Router()


def register_start_handlers(repo: StoreRepository) -> Router:
    @router.message(CommandStart())
    async def start_handler(message: Message) -> None:
        user = message.from_user
        if user:
            repo.add_user(user.id, user.username, user.first_name)
        await message.answer(
            "Welcome to *NovaStore* 🛒\n"
            "A modular Telegram shopping bot demo for employers.\n\n"
            "Tap a button below or use commands:\n"
            "`/catalog` `/cart` `/checkout`",
            parse_mode="Markdown",
            reply_markup=main_menu,
        )

    @router.message(F.text == "🛍 Browse Products")
    async def browse_button(message: Message) -> None:
        await message.answer("Use `/catalog` to view all products.", parse_mode="Markdown")

    @router.message(F.text == "🧺 My Cart")
    async def cart_button(message: Message) -> None:
        await message.answer("Use `/cart` to view your current cart.", parse_mode="Markdown")

    return router
