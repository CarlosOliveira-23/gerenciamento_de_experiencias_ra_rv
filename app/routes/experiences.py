from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.database import SessionLocal
from app.models.experience_db import ExperienceDB
from app.models.experience import Experience
from app.models.experience_logs import ExperienceLog
from app.auth import get_current_user
from app.routes.ranking import add_points

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/experiences", response_model=List[Experience])
def read_experiences(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """ Retorna todas as experiências da empresa do usuário """
    query = db.query(ExperienceDB).filter(ExperienceDB.nrorg == current_user["nrorg"])

    if category:
        query = query.filter(ExperienceDB.category == category)

    if tags:
        tags_list = tags.split(",")
        query = query.filter(ExperienceDB.tags.overlap(tags_list))

    return query.offset(skip).limit(limit).all()


@router.get("/experiences/{experience_id}", response_model=Experience)
def get_experience(experience_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """ Retorna os detalhes de uma experiência da empresa do usuário """
    experience = db.query(ExperienceDB).filter(
        ExperienceDB.id == experience_id,
        ExperienceDB.nrorg == current_user["nrorg"]
    ).first()

    if not experience:
        raise HTTPException(status_code=404, detail="Experiência não encontrada")

    log = ExperienceLog(experience_id=experience_id, user_id=current_user["username"], action="view")
    db.add(log)
    db.commit()

    return experience


@router.post("/experiences", response_model=Experience)
def create_experience(experience: Experience, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """ Cria uma nova experiência para a empresa do usuário """
    db_experience = ExperienceDB(**experience.dict(), nrorg=current_user["nrorg"])
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)

    log = ExperienceLog(experience_id=db_experience.id, user_id=current_user["username"], action="create")
    db.add(log)
    db.commit()

    return db_experience


@router.put("/experiences/{experience_id}", response_model=Experience)
def update_experience(
    experience_id: int,
    experience: Experience,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """ Atualiza uma experiência da empresa do usuário """
    db_experience = db.query(ExperienceDB).filter(
        ExperienceDB.id == experience_id,
        ExperienceDB.nrorg == current_user["nrorg"]
    ).first()

    if not db_experience:
        raise HTTPException(status_code=404, detail="Experiência não encontrada")

    for key, value in experience.dict(exclude_unset=True).items():
        setattr(db_experience, key, value)

    db.commit()
    db.refresh(db_experience)

    log = ExperienceLog(experience_id=experience_id, user_id=current_user["username"], action="update")
    db.add(log)
    db.commit()

    return db_experience


@router.delete("/experiences/{experience_id}")
def delete_experience(experience_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """ Exclui uma experiência da empresa do usuário """
    db_experience = db.query(ExperienceDB).filter(
        ExperienceDB.id == experience_id,
        ExperienceDB.nrorg == current_user["nrorg"]
    ).first()

    if not db_experience:
        raise HTTPException(status_code=404, detail="Experiência não encontrada")

    db.delete(db_experience)
    db.commit()

    log = ExperienceLog(experience_id=experience_id, user_id=current_user["username"], action="delete")
    db.add(log)
    db.commit()

    return {"message": "Experiência excluída com sucesso"}


@router.post("/experiences/{experience_id}/participate", response_model=dict)
def participate_experience(experience_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """ Registra a participação do usuário e adiciona pontos """
    experience = db.query(ExperienceDB).filter(
        ExperienceDB.id == experience_id,
        ExperienceDB.nrorg == current_user["nrorg"]
    ).first()

    if not experience:
        raise HTTPException(status_code=404, detail="Experiência não encontrada")

    add_points(db, current_user["username"], 20)

    return {"message": "Participação registrada com sucesso!"}
