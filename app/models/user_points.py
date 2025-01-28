from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class UserPoints(Base):
    __tablename__ = "user_points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)  # ID do usuário
    points = Column(Integer, default=0)  # Pontos acumulados pelo usuário

    user = relationship("User", backref="points")
