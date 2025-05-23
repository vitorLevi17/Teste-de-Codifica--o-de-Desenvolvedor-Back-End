from typing import List
from fastapi import APIRouter, Depends
from validate_docbr import CPF
from sqlalchemy.orm import Session
from models import models
from models.database import SessionLocal
from schemas.cliente import ClienteSchema,ClienteCriarSchema
from fastapi import HTTPException,status

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get('/',response_model=List[ClienteSchema])
def cliente(db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).all()
    return clientes

@router.post('/',response_model=ClienteSchema)
def criar_cliente(cliente: ClienteCriarSchema, db: Session = Depends(get_db)):
    cliente_novo = models.Cliente(**cliente.dict())
    db.add(cliente_novo)
    db.commit()
    db.refresh(cliente_novo)
    return cliente_novo
@router.put('/{cliente_id}',response_model=ClienteSchema)
def editar_cliente(cliente_id: int,cliente_put: ClienteCriarSchema, db:Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    for key, value in cliente_put.dict().items():
        setattr(cliente,key,value)

    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete('/{cliente_id}')
def excluir_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso"}