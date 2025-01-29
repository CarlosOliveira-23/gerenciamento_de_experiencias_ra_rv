from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import SessionLocal
from app.models.login_attempts import LoginAttempt

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login-attempts", response_model=List[dict])
def get_login_attempts(db: Session = Depends(get_db)):
    """ Retorna as últimas tentativas de login """
    attempts = db.query(LoginAttempt).order_by(LoginAttempt.timestamp.desc()).limit(20).all()
    return [
        {
            "id": attempt.id,
            "username": attempt.username,
            "ip_address": attempt.ip_address,
            "success": attempt.success,
            "timestamp": attempt.timestamp,
        }
        for attempt in attempts
    ]
