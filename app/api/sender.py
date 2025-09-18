# app/api/sender.py
from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.model.sender import Sender
from app.service.email_service import save_sender_if_new

router = APIRouter()


class SenderCreate(BaseModel):
    email: EmailStr


@router.post("/senders")
def add_sender(sender: SenderCreate, db: Session = Depends(get_db)):
    """
    Add a new sender if it does not exist.
    Returns the sender object.
    """
    new_sender = save_sender_if_new(db, sender.email)
    if not new_sender:
        raise HTTPException(status_code=400, detail="Failed to add sender")
    return {
        'message': 'successfully added sender'
        , 'success': True,
        'data': {
            "id": new_sender.id, "email": new_sender.email, "name": new_sender.name}

    }


@router.get("/senders")
def list_senders(request: Request, db: Session = Depends(get_db)):
    # Get front-end origin from headers
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")  # sometimes useful
    client_host = request.client.host  # client IP

    print(f"Request from origin: {origin}, referer: {referer}, IP: {client_host}")

   

    senders = db.query(Sender).all()
    return [{"id": s.id, "email": s.email, "name": s.name} for s in senders]
