from fastapi import HTTPException, status
import re
from datetime import datetime
from models import models
def validar_pedido(pedido,db):
    padrao_dt = r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
    if not db.query(models.Cliente).filter(models.Cliente.id == pedido.cliente_fk).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente não encontrado."
        )
    if not db.query(models.Produtos).filter(models.Produtos.id == pedido.produto_fk).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Produto não encontrado."
        )
    produto = db.query(models.Produtos).filter(models.Produtos.id == pedido.produto_fk).first()
    if pedido.quantidade_itens > produto.estoque_inicial:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A quantidade solicitada é maior que o estoque."
        )
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

