from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.routes import experiences
from app.routes.statistics import router as statistics_router
from app.routes.schedule import router as schedule_router
from app.routes.media import router as media_router
from app.routes.review import router as review_router
from app.routes.logs import router as logs_router
from app.routes.views import router as views_router
from app.routes.public_api import router as public_api_router
from app.routes.sync_ra_rv import router as sync_router
from app.routes.ranking import router as ranking_router
from app.routes.security import router as security_router
from app.utils.i18n import get_locale_from_request, translate

app = FastAPI(title="Gerenciador de Experiências RA/RV")

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(security_router, prefix="/security")
app.include_router(statistics_router, prefix="/stats")
app.include_router(schedule_router, prefix="/schedule")
app.include_router(media_router, prefix="/media")
app.include_router(review_router, prefix="/reviews")
app.include_router(logs_router, prefix="/logs")
app.include_router(views_router, prefix="/views")
app.include_router(public_api_router, prefix="/api")
app.include_router(sync_router, prefix="/sync")
app.include_router(ranking_router, prefix="/gamification")
app.include_router(experiences.router, prefix="/experiences")


@app.get("/")
def root(request: Request):
    lang = get_locale_from_request(request)
    return {"message": translate("Welcome to the RA/RV Experience Manager", lang)}
