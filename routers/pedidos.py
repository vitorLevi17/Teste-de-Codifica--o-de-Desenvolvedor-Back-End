from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import models
from models.models import Pedidos, Produtos,Item_Pedido
from schemas.pedidos import PedidoSchema,CriarPedidoSchema,EditarPedidoSchema
from models.database import SessionLocal
from auxiliars import validacoes
from auxiliars import validacoes_pedidos

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
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    resultado = []
    for pedido in pedidos:
        itens = db.query(Item_Pedido).filter(Item_Pedido.pedido_fk == pedido.id).all()
        resultado.append({
            "id": pedido.id,
            "cliente_fk": pedido.cliente_fk,
            "status": pedido.status,
            "periodo": pedido.periodo,
            "itens": [
                {"produto_id": item.produto_id_fk, "quantidade": item.quantidade}
                for item in itens
        ]
    })

    return resultado
@router.get('/{pedidos_id}',response_model=PedidoSchema)
def pedido_id(pedidos_id:int ,db:SessionLocal = Depends(get_db)):
    pedido = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()
    validacoes.validar_objeto_bd(pedido, pedidos_id)
    itens = db.query(Item_Pedido).filter(Item_Pedido.pedido_fk == pedidos_id).all()
    itens_schema = [{"produto_id": item.produto_id_fk, "quantidade": item.quantidade} for item in itens]

    pedido_completo = {
        "id": pedido.id,
        "cliente_fk": pedido.cliente_fk,
        "status": pedido.status,
        "periodo": pedido.periodo,
        "itens": itens_schema
    }
    return pedido_completo

@router.post('/')
def criar_pedido(pedidos: CriarPedidoSchema,db:SessionLocal = Depends(get_db)):
    validacoes_pedidos.validar_pedido(pedidos,db)
    pedido_post = Pedidos(cliente_fk = pedidos.cliente_fk,
                          status="Em preparação",
                          periodo=pedidos.periodo)
    db.add(pedido_post)
    db.commit()
    db.refresh(pedido_post)

    for item in pedidos.itens:
        item_pedido = Item_Pedido(
            pedido_fk = pedido_post.id,
            produto_id_fk = item.produto_id,
            quantidade = item.quantidade
        )
        db.add(item_pedido)
        produto = db.query(Produtos).filter(Produtos.id == item.produto_id).first()
        produto.estoque -= item.quantidade

    db.commit()
    return {"message": "Pedido criado com sucesso", "pedido_id": pedido_post.id}
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
    itens = db.query(Item_Pedido).filter(Item_Pedido.pedido_fk == pedidos_id).all()
    db.delete(pedidos)
    db.delete(itens)
    db.commit()
    return {"mensagem":"Pedido deletado com sucesso"}