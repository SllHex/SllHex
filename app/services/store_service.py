from __future__ import annotations

from app.core.utils import format_price
from app.repositories.store_repo import StoreRepository


class StoreService:
    def __init__(self, repo: StoreRepository) -> None:
        self.repo = repo

    def get_catalog_text(self) -> str:
        products = self.repo.list_products()
        if not products:
            return "No products available yet."

        lines = ["🛍 *Store Catalog*\n"]
        for product in products:
            lines.append(
                f"`{product['id']}` • *{product['name']}*\n"
                f"{product['description']}\n"
                f"Price: {format_price(product['price'])} | Stock: {product['stock']}\n"
            )
        lines.append("Use: `/add <product_id>` to add an item to your cart.")
        return "\n".join(lines)

    def get_cart_text_and_total(self, user_id: int) -> tuple[str, int]:
        items = self.repo.get_cart(user_id)
        if not items:
            return ("🧺 Your cart is empty.", 0)

        lines = ["🧺 *Your Cart*\n"]
        total = 0
        for item in items:
            subtotal = item["qty"] * item["price"]
            total += subtotal
            lines.append(
                f"• {item['name']} x{item['qty']} = {format_price(subtotal)}"
            )

        lines.append(f"\nTotal: *{format_price(total)}*")
        lines.append("Use `/checkout` to complete your order.")
        return ("\n".join(lines), total)
