from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.database import SessionLocal
from app.models.experience_db import ExperienceDB
from app.models.experience import Experience
from app.models.experience_logs import ExperienceLog

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


@router.get("/experiences/{experience_id}", response_model=Experience)
def get_experience(experience_id: int, db: Session = Depends(get_db)):
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    # Registrar o acesso à experiência
    log = ExperienceLog(experience_id=experience_id)
    db.add(log)
    db.commit()

    return experience


# Atualizacao de experiencia
@router.put("/experiences/{experience_id}", response_model=Experience)
def update_experience(experience_id: int, experience: Experience, user_id: int, db: Session = Depends(get_db)):
    db_experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    for key, value in experience.dict(exclude_unset=True).items():
        setattr(db_experience, key, value)

    db.commit()
    db.refresh(db_experience)

    log_experience_change(db, experience_id, user_id, "update")

    return db_experience


@router.delete("/experiences/{experience_id}")
def delete_experience(experience_id: int, user_id: int, db: Session = Depends(get_db)):
    db_experience = db.query(ExperienceDB).filter(ExperienceDB.id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    db.delete(db_experience)
    db.commit()

    log_experience_change(db, experience_id, user_id, "delete")

    return {"message": "Experience deleted successfully"}


@router.post("/experiences", response_model=Experience)
def create_experience(experience: Experience, user_id: int, db: Session = Depends(get_db)):
    db_experience = ExperienceDB(**experience.dict())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)

    log_experience_change(db, db_experience.id, user_id, "create")

    return db_experience


@router.get("/experiences/{id}", response_model=Experience)
def get_experience(id: int, user_id: int, db: Session = Depends(get_db)):
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    log_experience_view(db, id, user_id)

    return experience


@router.post("/experiences/{id}/participate", response_model=dict)
def participate_experience(id: int, user_id: int, db: Session = Depends(get_db)):
    """ Registra a participação do usuário em uma experiência e adiciona pontos """
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    # Adicionar pontos ao usuário pela participação
    add_points(db, user_id, 20)  # Exemplo: 20 pontos por participação

    return {"message": "Participation registered successfully!"}
