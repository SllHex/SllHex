from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path("data/store.db")


class Database:
    def __init__(self, path: Path = DB_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def init(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT
                );

                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS cart_items (
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    qty INTEGER NOT NULL DEFAULT 1,
                    PRIMARY KEY (user_id, product_id),
                    FOREIGN KEY(product_id) REFERENCES products(id)
                );

                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    status TEXT NOT NULL DEFAULT 'paid',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

    def seed_products(self) -> None:
        with self.connect() as conn:
            existing = conn.execute("SELECT COUNT(*) as count FROM products").fetchone()["count"]
            if existing:
                return
            conn.executemany(
                "INSERT INTO products(name, description, price, stock) VALUES (?, ?, ?, ?)",
                [
                    ("Nova Headphones", "Wireless noise-canceling headphones", 129, 12),
                    ("Hyper Mouse", "RGB ergonomic gaming mouse", 59, 20),
                    ("Flex Keyboard", "Low-profile mechanical keyboard", 99, 10),
                    ("Pulse Smartwatch", "Health tracking smartwatch", 149, 8),
                ],
            )
