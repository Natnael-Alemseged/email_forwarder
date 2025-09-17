# app/api/sender.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.model.sender import Sender

router = APIRouter()

@router.get("/senders")
def list_senders(db: Session = Depends(get_db)):
    senders = db.query(Sender).all()
    return [{"id": s.id, "email": s.email, "name": s.name} for s in senders]
