from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.model.user import User


user = APIRouter()

@user.post("/users")
def add_user(email: str, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return {"message": "User already exists", "id": existing_user.id}

    # Otherwise create new user
    new_user = User(email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User added", "id": new_user.id}