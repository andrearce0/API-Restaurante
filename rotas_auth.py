from modelos import UsuarioRegistroRequest
from repositorios import UsuarioRepositorio
from fastapi import APIRouter, HTTPException, status, Depends
from seguranca import verificar_senha, gerar_hash_senha, criar_token
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session

router_auth = APIRouter()

@router_auth.post("/usuarios/register", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioRegistroRequest, db: Session = Depends(get_db)):
    usuario_existente = UsuarioRepositorio.buscar_por_email(db, usuario.email)
    
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Já existe um usuário com o email informado."
        )
    
    senha_hash = gerar_hash_senha(usuario.senha)
    usuario.senha = senha_hash

    novo_usuario = UsuarioRepositorio.registrar(db, usuario)

    return novo_usuario

@router_auth.post("/usuarios/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = UsuarioRepositorio.buscar_por_email(db, form_data.username)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email e/ou senha incorreto(s).")

    senha_valida = verificar_senha(form_data.password, usuario.senha)

    if not senha_valida:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email e/ou senha incorreto(s).")
    
    token = criar_token({"sub": usuario.email})

    return {"access_token": token, "token_type": "bearer"}