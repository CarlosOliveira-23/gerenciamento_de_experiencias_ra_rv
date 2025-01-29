from app.models.database import Base, engine
from app.models.experience_db import ExperienceDB
from app.models.experience_logs import ExperienceLog
from app.models.schedule import ExperienceSchedule
from app.models.review import ExperienceReview
from app.models.experience_views import ExperienceView
from app.models.user_points import UserPoints
from app.models.login_attempts import LoginAttempt


Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
