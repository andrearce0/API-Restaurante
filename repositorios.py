from sqlalchemy.orm import Session
from modelos import CategoriaDB, CategoriaRequest, PratoDB, ItemCardapioRequest, UsuarioRegistroRequest, UsuarioDB

class CategoriaRepositorio:
    @staticmethod
    def salvar(db: Session, categoria: CategoriaRequest):
        nova_categoria = CategoriaDB(nome=categoria.nome, descricao=categoria.descricao)
        db.add(nova_categoria)
        db.commit()
        db.refresh(nova_categoria)

        return nova_categoria

    @staticmethod
    def buscar_todas(db: Session):
        return db.query(CategoriaDB).all()

class ItensCardapioRepositorio:
    @staticmethod
    def salvar(db: Session, item: ItemCardapioRequest):
        novo_item = PratoDB(nome=item.nome,
        descricao=item.descricao,
        preco=item.preco,
        disponivel=item.disponivel,
        categoria_id=item.categoria_id)

        db.add(novo_item)
        db.commit()
        db.refresh(novo_item)

        return novo_item

    @staticmethod
    def buscar_todos(db: Session):
        return db.query(PratoDB).all()

    @staticmethod
    def detalhar(db: Session, id_item: int):
        prato = db.query(PratoDB).filter(PratoDB.id == id_item).first()

        return prato
    
    @staticmethod
    def atualizar(db: Session, id_item: int, item_atualizado: ItemCardapioRequest):
        item = db.query(PratoDB).filter(PratoDB.id == id_item).first()

        if not item:
            return None
        
        item.nome = item_atualizado.nome
        item.categoria_id = item_atualizado.categoria_id
        item.descricao = item_atualizado.descricao
        item.preco = item_atualizado.preco
        item.disponivel = item_atualizado.disponivel
        
        db.commit()
        db.refresh(item)

        return item

class UsuarioRepositorio:
    @staticmethod
    def registrar(db: Session, usuario: UsuarioRegistroRequest):
        novo_usuario = UsuarioDB(nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha)

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return novo_usuario

    @staticmethod
    def buscar_por_email(db: Session, email: str):
        return db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
        