from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import SessionLocal
from app.models.experience_views import ExperienceView

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/experiences/views", response_model=List[dict])
def list_experience_views(db: Session = Depends(get_db)):
    views = db.query(ExperienceView).all()
    return [
        {
            "id": view.id,
            "experience_id": view.experience_id,
            "user_id": view.user_id,
            "viewed_at": view.viewed_at,
        }
        for view in views
    ]
