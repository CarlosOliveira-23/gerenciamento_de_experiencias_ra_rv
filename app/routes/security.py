from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import SessionLocal
from app.models.login_attempts import LoginAttempt

router = APIRouter()

# Configuração de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Gera um hash seguro para a senha"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado"""
    return pwd_context.verify(plain_password, hashed_password)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login-attempts", response_model=List[dict])
def get_login_attempts(db: Session = Depends(get_db)):
    """ Retorna as últimas tentativas de login """
    attempts = db.query(LoginAttempt).order_by(LoginAttempt.timestamp.desc()).limit(20).all()
    return [
        {
            "id": attempt.id,
            "username": attempt.username,
            "ip_address": attempt.ip_address,
            "success": attempt.success,
            "timestamp": attempt.timestamp,
        }
        for attempt in attempts
    ]
