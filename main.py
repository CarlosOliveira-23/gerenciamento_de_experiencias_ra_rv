from fastapi import FastAPI
from app.routes import experiences

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Gerenciador de Experiencias RA/RV"}


app.include_router(experiences.router)
