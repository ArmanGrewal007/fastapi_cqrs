from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import sqlite3

from app.api.deps import get_write_db, get_read_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.services import sync_write_to_read

user_router = APIRouter()


@user_router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_write_db),
):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Sync with read model asynchronously
    background_tasks.add_task(
        sync_write_to_read, db_user.id, db_user.name, db_user.email
    )

    return db_user


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db=Depends(get_read_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row["id"], "name": row["name"], "email": row["email"]}


@user_router.get("/", response_model=list[UserResponse])
def list_users(db=Depends(get_read_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    return [
        {"id": row["id"], "name": row["name"], "email": row["email"]} for row in users
    ]
