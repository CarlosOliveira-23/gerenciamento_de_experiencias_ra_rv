from fastapi import FastAPI
from app.routes import experiences
from app.models import experience
from app.routes.statistics import router as statistics_router

app = FastAPI()

app.include_router(statistics_router, prefix="/stats")


@app.get("/")
def root():
    return {"message": "Gerenciador de Experiencias RA/RV"}


app.include_router(experiences.router)
