from fastapi import FastAPI
from app.routes import experiences
from app.models import experience

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Gerenciador de Experiencias RA/RV"}


app.include_router(experiences.router)
