from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey 
from database import Base

class ItemCardapioRequest(BaseModel):
    nome: str
    categoria_id: int
    descricao: Optional[str] = None
    preco: float
    disponivel: bool = True

class ItemCardapioResponse(BaseModel):
    id: int
    nome: str
    categoria_id: int
    descricao: Optional[str] = None
    preco: float
    disponivel: bool = True

    class Config:
        from_attributes = True

class PratoDB(Base):
    __tablename__ = "Itens"

    id = Column(Integer, primary_key=True, index=True)
    categoria_id = Column(Integer, ForeignKey("Categorias.id"), nullable=False)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)
    disponivel = Column(Boolean, default=True)

class CategoriaRequest(BaseModel):
    nome: str
    descricao: Optional[str] = None

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None

    class Config:
        from_attributes = True

class CategoriaDB(Base):
    __tablename__ = "Categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)

class UsuarioRegistroRequest(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioLoginRequest(BaseModel):
    email: str
    senha:str

class UsuarioDB(Base):
    __tablename__ =  "Usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
