from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import sync_write_to_read, remove_user_from_read
from app.api.deps import get_write_db, get_read_db

user_router = APIRouter()


@user_router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_write_db),
):
    try:
        db_user = User(name=user.name, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Sync with read model asynchronously
        background_tasks.add_task(
            sync_write_to_read, db_user.id, db_user.name, db_user.email
        )

        return {"message": "User created successfully"}
    except Exception as e:
        return {"error": str(e)}


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db=Depends(get_read_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": row["id"], "name": row["name"], "email": row["email"]}
    except Exception as e:
        return {"error": str(e)}


@user_router.get("/", response_model=list[UserResponse])
def list_users(db=Depends(get_read_db)):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        return [
            {"id": row["id"], "name": row["name"], "email": row["email"]}
            for row in users
        ]
    except Exception as e:
        return {"error": str(e)}


@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_write_db),
):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.name = user_update.name
        db_user.email = user_update.email
        db.commit()
        db.refresh(db_user)

        # Sync the update to the read database asynchronously
        background_tasks.add_task(
            sync_write_to_read, db_user.id, db_user.name, db_user.email
        )

        return {"message": "User updated successfully"}
    except Exception as e:
        return {"error": str(e)}


@user_router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_write_db),
):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(db_user)
        db.commit()

        # Remove from read model asynchronously
        background_tasks.add_task(remove_user_from_read, user_id)

        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
