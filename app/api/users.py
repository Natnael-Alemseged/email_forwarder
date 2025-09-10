from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.model.user import User


user = APIRouter()

@user.post("/users")
def add_user(email: str, db: Session = Depends(get_db)):
    user = User(email=email)
    db.add(user)
    db.commit()
    return {"message": "User added", "id": user.id}