from fastapi import FastAPI

from app.core.config import settings
from app.core.database import init_db
from app.api.endpoints import user_router

app = FastAPI(title=settings.PROJECT_NAME)

# Initialize database
init_db()

# Include routers
app.include_router(user_router, prefix="/users", tags=["users"])
