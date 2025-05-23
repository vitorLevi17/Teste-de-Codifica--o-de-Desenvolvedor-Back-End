from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import models
from schemas.pedidos import PedidoSchema,CriarPedidoSchema,EditarPedidoSchema
from models.database import SessionLocal
from auxiliars import validacoes

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
    validacoes.validar_objeto_bd(pedido,pedidos_id)
    return pedido
@router.post('/',response_model=CriarPedidoSchema)
def criar_pedido(pedidos: CriarPedidoSchema,db:SessionLocal = Depends(get_db)):
    pedidos = models.Pedidos(**pedidos.dict(),status="Em preparação")
    db.add(pedidos)
    db.commit()
    db.refresh(pedidos)
    return pedidos
@router.put('/{pedidos_id}',response_model=PedidoSchema)
def editar_pedido(pedidos_id:int, pedido_put:EditarPedidoSchema, db:Session = Depends(get_db)):
    pedido = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()
    validacoes.validar_objeto_bd(pedido,pedidos_id)
    for key, value in pedido_put.dict().items():
        setattr(pedido,key,value)
    db.commit()
    db.refresh(pedido)
    return pedido
@router.delete('/{pedidos_id}')
def excluir_pedido(pedidos_id: int, db: Session = Depends(get_db)):
    pedidos = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()
    validacoes.validar_objeto_bd(pedidos,pedidos_id)
    db.delete(pedidos)
    db.commit()
    return {"mensagem":"Pedido deletado com sucesso"}