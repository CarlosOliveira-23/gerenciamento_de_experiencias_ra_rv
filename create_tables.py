from app.models.database import Base, engine
from app.models.experience_db import ExperienceDB
from app.models.experience_logs import ExperienceLog


Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
