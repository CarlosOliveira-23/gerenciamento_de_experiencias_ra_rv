from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base


class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    success = Column(Integer, nullable=False)  # 1 = sucesso, 0 = falha
    timestamp = Column(DateTime(timezone=True), default=func.now())
