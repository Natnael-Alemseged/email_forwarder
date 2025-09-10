from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db

from app.model.rule import Rule

router = APIRouter()

@router.post("/rules")
def add_rule(user_id: int, sender: str, db: Session = Depends(get_db)):
    rule = Rule(user_id=user_id, sender=sender)
    db.add(rule)
    db.commit()
    return {"message": "Rule added", "id": rule.id}