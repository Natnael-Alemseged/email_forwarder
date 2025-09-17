from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.model.rule import Rule
from app.model.user import User
from app.model.sender import Sender

router = APIRouter()

@router.post("/rules")
def add_rule(user_id: str, sender_id: str, db: Session = Depends(get_db)):
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate sender exists
    sender = db.query(Sender).filter(Sender.id == sender_id).first()
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")

    # Ensure rule is unique
    existing_rule = (
        db.query(Rule)
        .filter(Rule.user_id == user_id, Rule.sender_id == sender_id)
        .first()
    )
    if existing_rule:
        raise HTTPException(status_code=400, detail="Rule already exists")

    # Create rule
    rule = Rule(user_id=user_id, sender_id=sender_id)
    db.add(rule)
    db.commit()
    db.refresh(rule)

    return {"message": "Rule added", "id": rule.id}




# ✅ Get all rules
@router.get("/rules")
def get_rules(db: Session = Depends(get_db)):
    rules = db.query(Rule).all()
    return rules


# ✅ Get rules for a specific user
@router.get("/rules/{user_id}")
def get_rules_by_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    rules = db.query(Rule).filter(Rule.user_id == user_id).all()
    return rules