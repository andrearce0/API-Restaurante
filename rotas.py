from fastapi import APIRouter, HTTPException, status, Depends
from modelos import ItemCardapioRequest, ItemCardapioResponse, PratoDB, CategoriaRequest, CategoriaResponse, CategoriaDB, UsuarioDB
from database import get_db
from sqlalchemy.orm import Session
from repositorios import ItensCardapioRepositorio, CategoriaRepositorio
from seguranca import obter_usuario_atual

router = APIRouter()

@router.post("/itens", status_code=status.HTTP_201_CREATED, response_model=ItemCardapioResponse)
def adicionar_item(item: ItemCardapioRequest, db: Session = Depends(get_db), usuario_logado: UsuarioDB = Depends(obter_usuario_atual)):
    novo_item = ItensCardapioRepositorio.salvar(db, item)

    return novo_item

@router.get("/itens", response_model=list[ItemCardapioResponse])
def listar_cardapio(db: Session = Depends(get_db)):
    itens = ItensCardapioRepositorio.buscar_todos(db)

    return itens

@router.get("/itens/{id_item}", response_model=ItemCardapioResponse)
def detalhar_item(id_item: int, db: Session = Depends(get_db)):
    prato = ItensCardapioRepositorio.detalhar(db, id_item)

    if not prato:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prato não encontrado")

    return prato
    

@router.put("/itens/{id_item}", response_model=ItemCardapioResponse)
def atualizar_item(id_item: int, item_atualizado: ItemCardapioRequest, db: Session = Depends(get_db)):
    item = ItensCardapioRepositorio.atualizar(db, id_item, item_atualizado)

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prato não encontrado")

    return item

@router.delete("/itens/{id_item}")
def remover_item(id_item: int, db: Session = Depends(get_db)):
    item = db.query(PratoDB).filter(PratoDB.id == id_item).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prato não encontrado.")

    db.delete(item)
    db.commit()

    return{"mensagem": "Prato removido com sucesso"}

@router.post("/categorias", status_code=status.HTTP_201_CREATED, response_model=CategoriaResponse)
def criar_categoria(nova_categoria: CategoriaRequest, db: Session = Depends(get_db), usuario_logado: UsuarioDB = Depends(obter_usuario_atual)):
    cat = CategoriaRepositorio.salvar(db, nova_categoria)

    return cat

@router.get("/categorias", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = CategoriaRepositorio.buscar_todas(db)

    return categorias