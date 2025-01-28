from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import SessionLocal
from app.models.experience_logs import ExperienceLog

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/experiences/logs", response_model=List[dict])
def list_experience_logs(db: Session = Depends(get_db)):
    logs = db.query(ExperienceLog).all()
    return [
        {
            "id": log.id,
            "experience_id": log.experience_id,
            "user_id": log.user_id,
            "action": log.action,
            "timestamp": log.timestamp,
        }
        for log in logs
    ]
