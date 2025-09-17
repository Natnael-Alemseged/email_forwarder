# app/api/sender.py
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.model.sender import Sender

router = APIRouter()

# Allowed frontend domains
ALLOWED_ORIGINS = [
    "https://v0-next-js-frontend-seven-flame.vercel.app",
    "http://localhost:3000",
    "https://v0.app",
]

@router.get("/senders")
def list_senders(request: Request, db: Session = Depends(get_db)):
    """
    List all senders. Logs origin, referer, and client IP.
    Rejects requests from non-whitelisted origins.
    """
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")
    client_ip = request.client.host

    print(f"Frontend origin: {origin}")
    print(f"Referer: {referer}")
    print(f"Client IP: {client_ip}")

    # Optional: whitelist only certain frontends
    if origin not in ALLOWED_ORIGINS:
        raise HTTPException(status_code=403, detail=f"Origin '{origin}' not allowed")

    senders = db.query(Sender).all()
    return [{"id": s.id, "email": s.email, "name": s.name} for s in senders]
