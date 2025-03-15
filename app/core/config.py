from pydantic_settings import BaseSettings  # type: ignore
from pathlib import Path


class Settings(BaseSettings):
    # Database Names
    WRITE_DB_NAME: str = "write_db.db"
    READ_DB_NAME: str = "read_db.db"

    BASE_DIR: Path = Path(__file__).parent.parent
    WRITE_DB_PATH: str = f"{BASE_DIR}/{WRITE_DB_NAME}"
    READ_DB_PATH: str = f"{BASE_DIR}/{READ_DB_NAME}"
    
    WRITE_DB_URL: str = f"sqlite:///{BASE_DIR}/{WRITE_DB_NAME}"
    READ_DB_URL: str = f"sqlite:///{BASE_DIR}/{READ_DB_NAME}"

    # Other App Configs
    API_PREFIX: str = ""
    PROJECT_NAME: str = "CQRS FastAPI App"

    class Config:
        case_sensitive = True


settings = Settings()
