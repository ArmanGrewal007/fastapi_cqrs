from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

from app.core.config import settings

# SQLAlchemy write engine
write_engine = create_engine(
    settings.WRITE_DB_URL, connect_args={"check_same_thread": False}
)
WriteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=write_engine)

# SQLAlchemy base class
Base = declarative_base()


# Initialize databases
def init_db():
    # Create tables in write DB
    Base.metadata.create_all(bind=write_engine)

    # Initialize read DB
    conn = sqlite3.connect("read_db.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )
    conn.commit()
    conn.close()
