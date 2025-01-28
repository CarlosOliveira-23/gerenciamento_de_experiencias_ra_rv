from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import SessionLocal
from app.models.review import ExperienceReview
from app.models.experience_db import ExperienceDB
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.sql import func
from app.services.points import add_points


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Modelo Pydantic para criar avaliações
class ReviewCreate(BaseModel):
    user_id: int
    rating: int = Field(..., ge=1, le=5)  # Restrição: 1 a 5 estrelas
    comment: str | None = None


@router.post("/experiences/{id}/reviews", response_model=dict)
def create_review(id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    """ Adiciona uma avaliação e concede pontos ao usuário """
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    new_review = ExperienceReview(
        experience_id=id,
        user_id=review.user_id,
        rating=review.rating,
        comment=review.comment,
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    add_points(db, review.user_id, 10)

    return {"message": "Review added successfully", "review_id": new_review.id}


@router.get("/experiences/{id}/rating", response_model=dict)
def get_average_rating(id: int, db: Session = Depends(get_db)):
    average_rating = db.query(func.avg(ExperienceReview.rating))\
        .filter(ExperienceReview.experience_id == id)\
        .scalar()
    if average_rating is None:
        raise HTTPException(status_code=404, detail="No reviews found for this experience")
    return {"average_rating": round(average_rating, 2)}

