from __future__ import annotations

from typing import List

from app.db.database import Database


class StoreRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_user(self, user_id: int, username: str | None, first_name: str | None) -> None:
        with self.db.connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO users (id, username, first_name) VALUES (?, ?, ?)",
                (user_id, username or "", first_name or ""),
            )

    def list_products(self) -> List[dict]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
            return [dict(row) for row in rows]

    def get_product(self, product_id: int) -> dict | None:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            return dict(row) if row else None

    def add_to_cart(self, user_id: int, product_id: int) -> None:
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT qty FROM cart_items WHERE user_id = ? AND product_id = ?",
                (user_id, product_id),
            ).fetchone()
            if row:
                conn.execute(
                    "UPDATE cart_items SET qty = qty + 1 WHERE user_id = ? AND product_id = ?",
                    (user_id, product_id),
                )
            else:
                conn.execute(
                    "INSERT INTO cart_items(user_id, product_id, qty) VALUES (?, ?, 1)",
                    (user_id, product_id),
                )

    def get_cart(self, user_id: int) -> List[dict]:
        with self.db.connect() as conn:
            rows = conn.execute(
                """
                SELECT c.product_id, c.qty, p.name, p.price
                FROM cart_items c
                JOIN products p ON p.id = c.product_id
                WHERE c.user_id = ?
                ORDER BY c.product_id
                """,
                (user_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def clear_cart(self, user_id: int) -> None:
        with self.db.connect() as conn:
            conn.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))

    def create_order(self, user_id: int, total: int) -> int:
        with self.db.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO orders(user_id, total, status) VALUES (?, ?, 'paid')",
                (user_id, total),
            )
            return int(cursor.lastrowid)

    def create_product(self, name: str, description: str, price: int, stock: int) -> int:
        with self.db.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO products(name, description, price, stock) VALUES (?, ?, ?, ?)",
                (name, description, price, stock),
            )
            return int(cursor.lastrowid)
