from app.models.database import Base, engine
from app.models.experience_db import ExperienceDB


Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
