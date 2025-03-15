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

    # Initialize read DB manually
    # (they say that later it will be easier to decouple read and write db, 
    # using event bus/ message queue)
    conn = sqlite3.connect(settings.READ_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )
    cursor.execute("PRAGMA query_only = 1;") # Make it read-only
    conn.commit()
    conn.close()
