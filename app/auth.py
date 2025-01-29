from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, APIRouter, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.database import SessionLocal
from app.utils import verify_password, hash_password
from app.models.login_attempts import LoginAttempt
from fastapi.security import OAuth2PasswordBearer

# Configuração de Segurança
SECRET_KEY = "Teste_segredo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do FastAPI
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# **Função para obter o banco de dados**
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# **Modelos Pydantic**
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# **Registrar tentativas de login**
def log_login_attempt(db: Session, username: str, ip: str, success: bool):
    attempt = LoginAttempt(username=username, ip_address=ip, success=1 if success else 0)
    db.add(attempt)
    db.commit()

# **Autenticar usuário**
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return {"username": user.username, "role": user.role}

# **Criar um token de acesso**
def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# **Obter o usuário autenticado**
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        return {"username": username, "role": role}
    except JWTError:
        raise credentials_exception

# **Rota para Login**
@router.post("/login", response_model=Token)
def login_for_access_token(form_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """Processa login e registra tentativas"""
    ip = request.client.host
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        log_login_attempt(db, form_data.username, ip, False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    log_login_attempt(db, form_data.username, ip, True)

    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

# **Criar usuário**
@router.post("/users")
def create_user(username: str, password: str, role: str = "user", db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username já existe")

    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "role": new_user.role}

# **Rota protegida: Apenas para administradores**
@router.get("/admin")
def admin_only(current_user: dict = Depends(get_current_user)):
    """ Apenas administradores podem acessar essa rota """
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem acessar esta rota.")
    return {"message": "Bem-vindo, administrador!"}
