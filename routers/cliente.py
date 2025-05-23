from typing import List
from fastapi import APIRouter, Depends, Query
from auxiliars import validacoes
from sqlalchemy.orm import Session
from models import models
from models.database import SessionLocal
from schemas.cliente import ClienteSchema,ClienteCriarSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get('/',response_model=List[ClienteSchema])
def cliente(db: Session = Depends(get_db),skip: int = Query(0, ge=0),
            limit: int = Query(10, le=100),
            nome: str = Query(None),
            email: str = Query(None)
            ):

    query = db.query(models.Cliente)

    if nome:
        query = query.filter(models.Cliente.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(models.Cliente.email.ilike(f"%{email}%"))

    clientes = query.offset(skip).limit(limit).all()

    return clientes
@router.get('/{cliente_id}',response_model=ClienteSchema)
def cliente_id(cliente_id:int, db: SessionLocal = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    validacoes.validar_objeto_bd(cliente,cliente_id)
    return cliente

@router.post('/',response_model=ClienteSchema)
def criar_cliente(cliente: ClienteCriarSchema, db: Session = Depends(get_db)):
    cliente_novo = models.Cliente(**cliente.dict())
    validacoes.validar_cliente(cliente_novo,db)
    db.add(cliente_novo)
    db.commit()
    db.refresh(cliente_novo)
    return cliente_novo
@router.put('/{cliente_id}',response_model=ClienteSchema)
def editar_cliente(cliente_id: int,cliente_put: ClienteCriarSchema, db:Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    validacoes.validar_objeto_bd(cliente,cliente_id)
    cliente_dados_atualizados = cliente_put
    validacoes.validar_cliente_editar(cliente_dados_atualizados, db, cliente_id=cliente_id)

    for key, value in cliente_put.dict().items():
        setattr(cliente,key,value)

    db.commit()
    db.refresh(cliente)
    return cliente
@router.delete('/{cliente_id}')
def excluir_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    validacoes.validar_objeto_bd(cliente, cliente_id)
    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso"}