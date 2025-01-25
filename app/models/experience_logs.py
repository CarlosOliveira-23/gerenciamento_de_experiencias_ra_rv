from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base


class ExperienceLog(Base):
    __tablename__ = "experience_logs"

    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey("experiences.id"), nullable=False)
    accessed_at = Column(DateTime(timezone=True), default=func.now())
