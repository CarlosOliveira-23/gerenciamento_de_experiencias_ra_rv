from sqlalchemy import Column, Integer, String
from .database import Base

class ClientConfig(Base):
    __tablename__ = "client_config"

    id = Column(Integer, primary_key=True, index=True)
    nrorg = Column(Integer, unique=True, nullable=False)
    logo_url = Column(String, nullable=True)
    primary_color = Column(String, default="#000000")
    secondary_color = Column(String, default="#FFFFFF")
