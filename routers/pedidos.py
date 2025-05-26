from typing import List
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from models import models
from models.models import Pedidos, Produtos, Item_Pedido, Cliente
from schemas.pedidos import PedidoSchemaList,CriarPedidoSchema,EditarPedidoSchema,PedidoSchema
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

@router.get('/',response_model=List[PedidoSchemaList])
def pedidos(db:SessionLocal = Depends(get_db),skip: int = Query(0, ge=0),
            limit: int = Query(10,le=100),
            periodo: str=Query(None),
            status: str=Query(None),
            id_cliente: int=Query(None)):
    query_pedidos = db.query(models.Pedidos)
    if periodo:
        query_pedidos = query_pedidos.filter(models.Pedidos.periodo.ilike(f"%{periodo}%"))
    if id_cliente:
        query_pedidos = query_pedidos.filter(Pedidos.cliente_fk == id_cliente)
    if status:
        query_pedidos = query_pedidos.filter(models.Pedidos.status.ilike(f"%{status}%"))

    query = query_pedidos.offset(skip).limit(limit)

    pedidos = query.all()

    resultado = []
    for pedido in pedidos:
        itens = db.query(Item_Pedido).filter(Item_Pedido.pedido_fk == pedido.id).all()
        produtos = db.query(Produtos).join(Item_Pedido).filter(Item_Pedido.pedido_fk == pedido.id).all()
        cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_fk).first()
        resultado.append({
            "id": pedido.id,
            "cliente_fk": pedido.cliente_fk,
            "status": pedido.status,
            "periodo": pedido.periodo,
            "itens": [{"produto_id": item.produto_id_fk, "quantidade": item.quantidade}for item in itens],
            "produto": [{"nome_produto": produto.nome_produto,"categoria": produto.categoria,
                     "preco": produto.preco,"descricao": produto.descricao,
                     "secao": produto.secao,"imagem": produto.imagem} for produto in produtos],
             "cliente":{"nome": cliente.nome,"telefone": cliente.telefone,"email":cliente.email},
    })
    return resultado
@router.get('/{pedidos_id}',response_model=PedidoSchemaList)
def pedido_id(pedidos_id:int ,db:SessionLocal = Depends(get_db)):
    pedido = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()
    produtos = db.query(Produtos).join(Item_Pedido).filter(Item_Pedido.pedido_fk == pedidos_id).all()
    cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_fk).first()
    validacoes.validar_objeto_bd(pedido, pedidos_id)
    itens = db.query(Item_Pedido).filter(Item_Pedido.pedido_fk == pedidos_id).all()

    pedido_completo = {
        "id": pedido.id,
        "cliente_fk": pedido.cliente_fk,
        "status": pedido.status,
        "periodo": pedido.periodo,
        "itens": [{"produto_id": item.produto_id_fk, "quantidade": item.quantidade}for item in itens],
        "produto": [{"nome_produto": produto.nome_produto, "categoria": produto.categoria,
                     "preco": produto.preco, "descricao": produto.descricao,
                     "secao": produto.secao, "imagem": produto.imagem} for produto in produtos],
        "cliente": {"nome": cliente.nome, "telefone": cliente.telefone, "email": cliente.email},
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
    for item in itens:
        db.delete(item)
    db.delete(pedidos)
    db.commit()
    return {"mensagem":"Pedido deletado com sucesso"}