from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.model.rule import Rule
from app.model.user import User
from app.model.sender import Sender

router = APIRouter()


# Create a rule
@router.post("/rules")
def add_rule(user_id: str, sender_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sender = db.query(Sender).filter(Sender.id == sender_id).first()
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")

    existing_rule = db.query(Rule).filter(Rule.user_id == user_id, Rule.sender_id == sender_id).first()
    if existing_rule:
        raise HTTPException(status_code=400, detail="Rule already exists")

    rule = Rule(user_id=user_id, sender_id=sender_id)
    db.add(rule)
    db.commit()
    db.refresh(rule)

    return {"message": "Rule added", "id": rule.id}


# Get all rules
@router.get("/rules")
def get_rules(db: Session = Depends(get_db)):
    rules = db.query(Rule).all()
    result = []
    for rule in rules:
        user = db.query(User).filter(User.id == rule.user_id).first()
        sender = db.query(Sender).filter(Sender.id == rule.sender_id).first()
        result.append({
            "rule_id": rule.id,
            "user": {"id": user.id, "email": user.email} if user else None,
            "sender": {"id": sender.id, "email": sender.email, "name": sender.name} if sender else None,
        })
    return {"status": "success", "data": result}


# Get rules for a specific user
@router.get("/rules/user/{user_id}")
def get_rules_by_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    rules = db.query(Rule).filter(Rule.user_id == user_id).all()
    result = []
    for rule in rules:
        sender = db.query(Sender).filter(Sender.id == rule.sender_id).first()
        result.append({
            "rule_id": rule.id,
            "sender": {"id": sender.id, "email": sender.email, "name": sender.name} if sender else None
        })
    return {"status": "success", "user": {"id": user.id, "email": user.email}, "data": result}


# Update a rule (change sender)
@router.put("/rules/{rule_id}")
def update_rule(rule_id: str, new_sender_id: str, db: Session = Depends(get_db)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    new_sender = db.query(Sender).filter(Sender.id == new_sender_id).first()
    if not new_sender:
        raise HTTPException(status_code=404, detail="Sender not found")

    # Ensure new rule combination doesn't exist already
    existing_rule = db.query(Rule).filter(Rule.user_id == rule.user_id, Rule.sender_id == new_sender_id).first()
    if existing_rule:
        raise HTTPException(status_code=400, detail="Rule with this sender already exists for user")

    rule.sender_id = new_sender_id
    db.commit()
    db.refresh(rule)

    return {"status": "success", "message": "Rule updated", "rule_id": rule.id}


# Delete a rule
@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: str, db: Session = Depends(get_db)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()
    return {"status": "success", "message": "Rule deleted", "rule_id": rule.id}