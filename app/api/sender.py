# app/api/sender.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.model.sender import Sender

router = APIRouter()

@router.get("/senders")
def list_senders(request: Request, db: Session = Depends(get_db)):
    # Get front-end origin from headers
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")  # sometimes useful
    client_host = request.client.host  # client IP

    print(f"Request from origin: {origin}, referer: {referer}, IP: {client_host}")

    # Optional: whitelist only certain frontends
    allowed_origins = [
        "https://v0-next-js-frontend-seven-flame.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "https://v0.app",
    ]
    if origin not in allowed_origins:
        raise HTTPException(status_code=403, detail="Origin not allowed")

    senders = db.query(Sender).all()
    return [{"id": s.id, "email": s.email, "name": s.name} for s in senders]