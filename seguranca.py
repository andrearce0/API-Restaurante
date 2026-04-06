import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from database import get_db
from repositorios import UsuarioRepositorio

SECRET_KEY = "5Mhm11f7SltJoti4be5HjgMWlnn15fojw0xEQ2tRmgfgCUDQAD"
ALGORITHM = "HS256"
TEMPO_EXPIRACAO_MINUTOS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

def criar_token(dados: dict):
    dados_copia = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO_MINUTOS)
    dados_copia.update({"exp": expiracao})

    token_codificado = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)
    return token_codificado

def gerar_hash_senha(senha: str) -> str:
    salt = bcrypt.gensalt()
    senha_hash_bytes = bcrypt.hashpw(senha.encode('utf-8'), salt)

    return senha_hash_bytes.decode('utf-8')

def verificar_senha(senha_texto_plano: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha_texto_plano.encode('utf-8'), senha_hash.encode('utf-8'))

def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")

        if email is None:
            raise credenciais_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Faça login novamente.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except jwt.InvalidTokenError:
        raise credenciais_exception

    usuario = UsuarioRepositorio.buscar_por_email(db, email=email)

    if usuario is None:
        raise credenciais_exception
    
    return usuario
