from sqlalchemy.orm import Session
from app.models.user_points import UserPoints


def add_points(db: Session, user_id: int, points: int):
    """ Adiciona pontos ao usuário no sistema de gamificação """
    user_points = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()

    if user_points:
        user_points.points += points
    else:
        user_points = UserPoints(user_id=user_id, points=points)
        db.add(user_points)

    db.commit()
    db.refresh(user_points)
    return user_points
