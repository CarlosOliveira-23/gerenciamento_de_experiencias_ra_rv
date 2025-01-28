from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.experience_db import ExperienceDB

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/sync/experiences", response_model=list[dict])
def sync_experiences(db: Session = Depends(get_db)):
    """ Rota para dispositivos RA/RV sincronizarem experiências """
    experiences = db.query(ExperienceDB).all()

    return [
        {
            "id": experience.id,
            "title": experience.title,
            "description": experience.description,
            "type": experience.type,
            "category": experience.category,
            "created_at": experience.created_at
        }
        for experience in experiences
    ]
