from typing import List
from pydantic import BaseModel
from schemas.cliente import ClienteSchemaPedido
from schemas.produto import ProdutoSchemaPedido
"""
    Schemas relacionados aos pedidos e seus itens
"""
#Gerenciar os itens do pedido
class ItemPedido(BaseModel):
    produto_id : int
    quantidade : int


class PedidoSchema(BaseModel):
    id : int
    cliente_fk : int
    status : str
    periodo : str

#Tudo relacionado ao pedido
class PedidoSchemaList(BaseModel):
    id : int
    cliente_fk : int
    status : str
    periodo : str
    itens: List[ItemPedido]
    produto: List[ProdutoSchemaPedido]
    cliente: ClienteSchemaPedido

#Schema para criar o pedido
class CriarPedidoSchema(BaseModel):
    cliente_fk : int
    periodo : str
    itens: List[ItemPedido]

#Schema para editar o pedido
class EditarPedidoSchema(BaseModel):
    cliente_fk : int
    status : str
    periodo : str
    itens: List[ItemPedido]

