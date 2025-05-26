from fastapi import HTTPException, status
import re
from datetime import datetime
from models import models
from models.models import Produtos

def validar_pedido(pedido,db):
    if not db.query(models.Cliente).filter(models.Cliente.id == pedido.cliente_fk).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente não encontrado, insira outro."
        )
    padrao_dt = r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
    if not re.match(padrao_dt,pedido.periodo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O periodo deve ter formato dd/mm/yyyy."
        )
    dt_validade = datetime.strptime(pedido.periodo, "%d/%m/%Y")
    if dt_validade <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O periodo deve ser maior que a data atual."
        )
    for item in pedido.itens:
        produto = db.query(Produtos).filter(Produtos.id == item.produto_id).first()
        if not produto:
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item.produto_id} não encontrado."
            )
        if produto.estoque < item.quantidade or produto.estoque == 0:
            raise HTTPException(status_code=400,
                                detail=f"Estoque insuficiente para o produto {item.produto_id}."
                                )
        if produto.disponivel_s_n == "Não":
            raise HTTPException(status_code=400,
                                detail=f"O produto {item.produto_id} não está disponivel para comercializar, insira outro."
                                )

def validar_pedido_editar(pedido,db):
    if not db.query(models.Cliente).filter(models.Cliente.id == pedido.cliente_fk).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente não encontrado, insira outro."
        )
    if pedido.status not in ["Em preparação","Finalizado","Cancelado"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido, selecione entre Finalizado e Cancelado."
        )
    padrao_dt = r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
    if not re.match(padrao_dt,pedido.periodo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O periodo deve ter formato dd/mm/yyyy."
        )
    dt_validade = datetime.strptime(pedido.periodo, "%d/%m/%Y")
    if dt_validade <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O periodo deve ser maior que a data atual."
        )
    for item in pedido.itens:
        produto = db.query(Produtos).filter(Produtos.id == item.produto_id).first()
        if not produto:
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item.produto_id} não encontrado."
            )
        if produto.estoque < item.quantidade or produto.estoque == 0:
            raise HTTPException(status_code=400,
                                detail=f"Estoque insuficiente para o produto {item.produto_id}."
                                )
        if produto.disponivel_s_n == "Não":
            raise HTTPException(status_code=400,
                                detail=f"O produto {item.produto_id} não está disponivel para comercializar, insira outro."
                                )