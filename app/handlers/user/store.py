from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.animation import animate_green_progress
from app.repositories.store_repo import StoreRepository
from app.services.store_service import StoreService

router = Router()


def register_store_handlers(repo: StoreRepository, service: StoreService) -> Router:
    @router.message(Command("catalog"))
    async def catalog_handler(message: Message) -> None:
        await message.answer(service.get_catalog_text(), parse_mode="Markdown")

    @router.message(Command("add"))
    async def add_handler(message: Message) -> None:
        user = message.from_user
        if not user:
            return

        parts = (message.text or "").split()
        if len(parts) != 2 or not parts[1].isdigit():
            await message.answer("Usage: `/add <product_id>`", parse_mode="Markdown")
            return

        product_id = int(parts[1])
        product = repo.get_product(product_id)
        if not product:
            await message.answer("❌ Product not found.")
            return

        repo.add_to_cart(user.id, product_id)
        await message.answer(f"✅ Added *{product['name']}* to your cart.", parse_mode="Markdown")

    @router.message(Command("cart"))
    async def cart_handler(message: Message) -> None:
        user = message.from_user
        if not user:
            return
        text, _ = service.get_cart_text_and_total(user.id)
        await message.answer(text, parse_mode="Markdown")

    @router.message(Command("checkout"))
    async def checkout_handler(message: Message) -> None:
        user = message.from_user
        if not user:
            return

        cart_text, total = service.get_cart_text_and_total(user.id)
        if total == 0:
            await message.answer(cart_text)
            return

        progress_message = await message.answer("Initializing payment...")
        await animate_green_progress(
            progress_message,
            title="🟢 Secure payment in progress",
            steps=10,
            delay=0.18,
        )

        order_id = repo.create_order(user.id, total)
        repo.clear_cart(user.id)
        await progress_message.edit_text(
            "✅ *Payment successful!*\n"
            f"Order ID: `{order_id}`\n"
            "Thank you for shopping with NovaStore.",
            parse_mode="Markdown",
        )

    return router
