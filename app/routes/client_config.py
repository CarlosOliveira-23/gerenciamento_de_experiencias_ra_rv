from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.client_config import ClientConfig
from app.models.database import SessionLocal
from app.auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/config")
def get_client_config(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Retorna as configurações personalizadas da empresa do usuário"""
    config = db.query(ClientConfig).filter(ClientConfig.nrorg == current_user["nrorg"]).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    return config


@router.post("/config")
def update_client_config(config: ClientConfig, db: Session = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    """Atualiza as configurações da empresa"""
    existing_config = db.query(ClientConfig).filter(ClientConfig.nrorg == current_user["nrorg"]).first()

    if existing_config:
        existing_config.logo_url = config.logo_url
        existing_config.primary_color = config.primary_color
        existing_config.secondary_color = config.secondary_color
    else:
        new_config = ClientConfig(nrorg=current_user["nrorg"], **config.dict())
        db.add(new_config)

    db.commit()
    return {"message": "Configuração atualizada com sucesso"}
