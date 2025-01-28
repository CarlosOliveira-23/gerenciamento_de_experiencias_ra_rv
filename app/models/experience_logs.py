from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class ExperienceLog(Base):
    __tablename__ = "experience_logs"

    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey("experiences.id"), nullable=False)
    user_id = Column(Integer, nullable=False)  # Quem fez a alteração
    action = Column(String, nullable=False)  # create, update, delete
    timestamp = Column(DateTime(timezone=True), default=func.now())  # Data e hora

    # Relacionamento com a experiência
    experience = relationship("ExperienceDB", backref="logs")
