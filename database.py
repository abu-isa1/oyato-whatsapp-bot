
import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_FILE = Path(__file__).with_name("oyato.db")


@contextmanager
def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                measurements TEXT NOT NULL,
                item TEXT NOT NULL,
                fabric TEXT NOT NULL,
                style TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK (
                        status IN (
                            'Pending',
                            'In Progress',
                            'Completed'
                        )
                    )
            )
        """)


def save_order(order):
    customer = order.customer

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO orders (
                order_id,
                customer_name,
                phone,
                measurements,
                item,
                fabric,
                style,
                price,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order.order_id,
            customer.name,
            customer.phone,
            customer.measurements,
            order.item,
            order.fabric,
            order.style,
            order.price,
            order.status
        ))


def get_all_orders():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM orders ORDER BY order_id
        """).fetchall()

        return [dict(row) for row in rows]
    

def search_orders_by_phone(phone):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM orders
            WHERE phone = ?
            ORDER BY order_id
        """, (phone,)).fetchall()

        return [dict(row) for row in rows]



def update_status(order_id, status):
    allowed_statuses = {
        "Pending",
        "In Progress",
        "Completed"
    }

    if status not in allowed_statuses:
        raise ValueError("Invalid order status.")

    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE orders
            SET status = ?
            WHERE order_id = ?
        """, (status, order_id))

        return cursor.rowcount > 0


def generate_order_id():
    with get_connection() as connection:
        row = connection.execute("""
            SELECT MAX(CAST(SUBSTR(order_id, 5) AS INTEGER))
            FROM orders
            WHERE order_id GLOB 'OYA-[0-9]*'
        """).fetchone()

        highest_number = row[0] or 0

    return f"OYA-{highest_number + 1:04d}"
