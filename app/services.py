import sqlite3


def sync_write_to_read(user_id: int, name: str, email: str) -> None:
    """
    Sync user data from write model to read model
    """
    conn = sqlite3.connect("read_db.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO users (id, name, email) VALUES (?, ?, ?)",
        (user_id, name, email),
    )
    conn.commit()
    conn.close()
