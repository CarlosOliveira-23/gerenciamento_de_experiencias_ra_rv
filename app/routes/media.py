from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.media import Media
from app.models.experience_db import ExperienceDB
from app.models.database import SessionLocal
import os
from uuid import uuid4

router = APIRouter()

MEDIA_DIRECTORY = "media/"  # Diretório onde os arquivos serão salvos
os.makedirs(MEDIA_DIRECTORY, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/experiences/{id}/media")
async def upload_media(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Verificar se a experiência existe
    experience = db.query(ExperienceDB).filter(ExperienceDB.id == id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    # Salvar o arquivo no diretório de mídia
    file_extension = file.filename.split(".")[-1]
    unique_file_name = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(MEDIA_DIRECTORY, unique_file_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Registrar a mídia no banco de dados
    media = Media(
        experience_id=id,
        file_name=file.filename,
        file_type=file.content_type.split("/")[0],  # Ex: "image", "video"
        file_url=f"/media/{unique_file_name}",
    )
    db.add(media)
    db.commit()
    db.refresh(media)

    return {"message": "File uploaded successfully", "media_id": media.id}


@router.get("/experiences/{id}/media", response_model=list[dict])
def list_media(id: int, db: Session = Depends(get_db)):
    media_files = db.query(Media).filter(Media.experience_id == id).all()
    return [
        {
            "id": media.id,
            "file_name": media.file_name,
            "file_type": media.file_type,
            "file_url": media.file_url,
        }
        for media in media_files
    ]

