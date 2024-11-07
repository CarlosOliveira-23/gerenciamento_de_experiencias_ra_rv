from sqlalchemy import Column, Integer, String, Date
from .database import Base


class ExperienceDB(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    type = Column(String)
    requirements = Column(String)
    created_at = Column(Date)
