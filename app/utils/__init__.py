from passlib.context import CryptContext

# Configuração para hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Gera um hash seguro para a senha"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado"""
    return pwd_context.verify(plain_password, hashed_password)
