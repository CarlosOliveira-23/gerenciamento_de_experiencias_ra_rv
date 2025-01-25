from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class ExperienceSchedule(Base):
    __tablename__ = "experience_schedules"

    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey("experiences.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)

    experience = relationship("ExperienceDB", backref="schedules")
