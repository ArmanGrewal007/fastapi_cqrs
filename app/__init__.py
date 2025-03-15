from fastapi import FastAPI, Request
from app.core.config import settings
from app.core.database import init_db
from app.api.endpoints import user_router
from app.middleware import LogMiddleware

app = FastAPI(title=settings.PROJECT_NAME)
init_db()
# Include routers
app.include_router(user_router, prefix="/users", tags=["users"])

app.add_middleware(LogMiddleware)
