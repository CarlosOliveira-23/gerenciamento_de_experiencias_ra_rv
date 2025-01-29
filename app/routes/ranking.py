from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.user_points import UserPoints
from app.models.user import User
from typing import List


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_points(db: Session, user_id: int, points: int):
    """ Adiciona pontos ao usuário pelo ID do usuário """
    user_points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
    if user_points:
        user_points.points += points
    else:
        user_points = UserPoints(user_id=user_id, points=points)
        db.add(user_points)
    db.commit()
    return {"message": f"{points} pontos adicionados para o usuário {user_id}"}


@router.get("/ranking", response_model=List[dict])
def get_ranking(db: Session = Depends(get_db)):
    """ Retorna um ranking com os usuários mais engajados """
    ranking = db.query(UserPoints).order_by(UserPoints.points.desc()).limit(10).all()

    return [
        {
            "user_id": user.user_id,
            "points": user.points
        }
        for user in ranking
    ]
