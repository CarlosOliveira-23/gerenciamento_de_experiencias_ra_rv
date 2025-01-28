from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import SessionLocal
from app.models.user_points import UserPoints
from app.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
