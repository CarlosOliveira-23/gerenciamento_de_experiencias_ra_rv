from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import SessionLocal
from app.models.schedule import ExperienceSchedule
from app.models.experience_db import ExperienceDB
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ScheduleCreate(BaseModel):
    experience_id: int
    scheduled_at: datetime
    user_id: int


# Criar um novo agendamento
@router.post("/schedules", response_model=dict)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    # Verificar se a experiência existe
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == schedule.experience_id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    # Verificar se já existe um agendamento para a mesma data/horário
    conflicting_schedule = db.query(ExperienceSchedule).filter(
        ExperienceSchedule.experience_id == schedule.experience_id,
        ExperienceSchedule.scheduled_at == schedule.scheduled_at,
    ).first()

    if conflicting_schedule:
        raise HTTPException(status_code=400, detail="Schedule conflict for the selected date and time")

    # Criar o agendamento
    new_schedule = ExperienceSchedule(
        experience_id=schedule.experience_id,
        scheduled_at=schedule.scheduled_at,
        user_id=schedule.user_id
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    return {"message": "Schedule created successfully", "id": new_schedule.id}


# Listar todos os agendamentos
@router.get("/schedules", response_model=List[dict])
def list_schedules(db: Session = Depends(get_db)):
    schedules = db.query(ExperienceSchedule).all()
    return [
        {
            "id": schedule.id,
            "experience_id": schedule.experience_id,
            "scheduled_at": schedule.scheduled_at,
            "user_id": schedule.user_id
        }
        for schedule in schedules
    ]


# Cancelar um agendamento
@router.delete("/schedules/{schedule_id}", response_model=dict)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(ExperienceSchedule).filter(ExperienceSchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    db.delete(schedule)
    db.commit()
    return {"message": "Schedule canceled successfully"}
