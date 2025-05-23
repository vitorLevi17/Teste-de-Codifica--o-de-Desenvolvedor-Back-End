from typing import List
from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from models import models
from schemas.pedidos import PedidoSchema,CriarPedidoSchema
from models.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[PedidoSchema])
def pedidos(db:SessionLocal = Depends(get_db)):
    pedidos = db.query(models.Pedidos).all()
    return pedidos

@router.get('/{pedidos_id}',response_model=PedidoSchema)
def pedido_id(pedidos_id:int ,db:SessionLocal = Depends(get_db)):
    pedido = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido com ID{pedidos_id} não encontrado"
        )
    return pedido

@router.post('/',response_model=CriarPedidoSchema)
def criar_pedido(pedidos: CriarPedidoSchema,db:SessionLocal = Depends(get_db)):
    pedidos = models.Pedidos(**pedidos.dict(),status="Em preparação")
    db.add(pedidos)
    db.commit()
    db.refresh(pedidos)
    return pedidos

@router.delete('/{pedidos_id}')
def excluir_pedido(pedidos_id: int, db: Session = Depends(get_db)):
    pedidos = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()
    if pedidos is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {pedidos_id} não encontrado"
        )
    db.delete(pedidos)
    db.commit()
    return {"mensagem":"Pedido deletado com sucesso"}




