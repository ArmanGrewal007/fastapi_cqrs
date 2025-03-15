import sqlite3
from typing import Generator
from app.core.config import settings

from app.core.database import WriteSessionLocal

def get_write_db() -> Generator:
    db = WriteSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_read_db() -> Generator:
    db = sqlite3.connect(settings.READ_DB_PATH)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()