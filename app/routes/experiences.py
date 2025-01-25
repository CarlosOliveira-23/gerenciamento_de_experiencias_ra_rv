from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.database import SessionLocal
from app.models.experience_db import ExperienceDB
from app.models.experience import Experience

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/experiences", response_model=list[Experience])
def read_experiences(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ExperienceDB)

    if category:
        query = query.filter(ExperienceDB.category == category)

    if tags:
        tags_list = tags.split(",")
        query = query.filter(ExperienceDB.tags.overlap(tags_list))

    return query.offset(skip).limit(limit).all()



# Atualizacao de experiencia
@router.put("/experiences/{experience_id}", response_model=Experience)
def update_experience(experience_id: int, experience: Experience, db: Session = Depends(get_db)):
    db_experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")

    for key, value in experience.dict(exclude_unset=True).items():
        setattr(db_experience, key, value)

    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.delete("/experiences/{experience_id}", response_model=Experience)
def delete_experience(experience_id: int, db: Session = Depends(get_db)):
    db_experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    db.delete(db_experience)
    db.commit()
    return db_experience
