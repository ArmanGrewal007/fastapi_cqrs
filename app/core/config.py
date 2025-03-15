from pydantic_settings import BaseSettings  # type: ignore


class Settings(BaseSettings):
    WRITE_DB_URL: str = "sqlite:///./write_db.db"
    READ_DB_URL: str = "sqlite:///./read_db.db"
    API_PREFIX: str = ""
    PROJECT_NAME: str = "CQRS FastAPI App"

    class Config:
        case_sensitive = True


settings = Settings()
