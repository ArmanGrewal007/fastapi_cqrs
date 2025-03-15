import sqlite3
from app.core.config import settings


def sync_write_to_read(user_id: int, name: str, email: str):
    conn = sqlite3.connect(settings.READ_DB_PATH)
    cursor = conn.cursor()

    # Check if user already exists in read DB
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:  # If user exists, update their details
        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id)
        )
    else:  # Otherwise, insert new user
        cursor.execute(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
            (user_id, name, email),
        )

    conn.commit()
    conn.close()


def remove_user_from_read(user_id: int):
    conn = sqlite3.connect(settings.READ_DB_PATH)
    cursor = conn.cursor()

    # Delete user from read DB
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()
