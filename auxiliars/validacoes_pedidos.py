from fastapi import HTTPException, status
import re
from datetime import datetime
from models import models
from models.models import Produtos
"""
    Esse metodo busca realizar as validações na criação e edição de pedidos
"""

def validar_pedido(pedido,db):
    #Validar se o cliente informado existe no banco de dados, caso não, o sistema lança a excessão
    if not db.query(models.Cliente).filter(models.Cliente.id == pedido.cliente_fk).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cliente não encontrado, insira outro."
        )
    #padrão de data que deve ser seguido
    padrao_dt = r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
    # Validar se o padrão da data está sendo seguido,caso não, o sistema lança a excessão
    if not re.match(padrao_dt,pedido.periodo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O periodo deve ter formato dd/mm/yyyy."
        )
    # Validar se a data é maior que o dia de hoje
    dt_validade = datetime.strptime(pedido.periodo, "%d/%m/%Y")
    if dt_validade <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O periodo deve ser maior que a data atual."
        )
    #Vallidar se os produtos especificados estão no banco de dados, para ver todos os produtos, é necessario usar um loop para percorrer todos os itens do pedido
    #Além de conferir se a quantidade está de acordo com o estoque e se o produto está disponivel
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
#Esse metodo segue a mesma logica do metodo acima, porem, checando o id para que a duplicidade não seja confundida
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