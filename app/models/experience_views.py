from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class ExperienceView(Base):
    __tablename__ = "experience_views"

    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey("experiences.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    viewed_at = Column(DateTime(timezone=True), default=func.now())

    # Relacionamento com a experiência
    experience = relationship("ExperienceDB", backref="views")
