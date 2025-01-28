from fastapi import FastAPI
from app.routes import experiences
from app.models import experience
from app.routes.statistics import router as statistics_router
from app.routes.schedule import router as schedule_router
from fastapi.staticfiles import StaticFiles
from app.routes.media import router as media_router
from app.routes.review import router as review_router
from app.routes.logs import router as logs_router
from app.routes.views import router as views_router

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(statistics_router, prefix="/stats")
app.include_router(schedule_router, prefix="/schedule")
app.include_router(media_router, prefix="/media")
app.include_router(review_router, prefix="/reviews")
app.include_router(logs_router, prefix="/logs")
app.include_router(views_router, prefix="/views")


@app.get("/")
def root():
    return {"message": "Gerenciador de Experiencias RA/RV"}


app.include_router(experiences.router)
