from typing import List
from pydantic import BaseModel
from schemas.cliente import ClienteSchemaPedido
from schemas.produto import ProdutoSchemaPedido

class ItemPedido(BaseModel):
    produto_id : int
    quantidade : int

class PedidoSchema(BaseModel):
    id : int
    cliente_fk : int
    status : str
    periodo : str
class PedidoSchemaList(BaseModel):
    id : int
    cliente_fk : int
    status : str
    periodo : str
    itens: List[ItemPedido]
    produto: List[ProdutoSchemaPedido]
    cliente: ClienteSchemaPedido

class CriarPedidoSchema(BaseModel):
    cliente_fk : int
    periodo : str
    itens: List[ItemPedido]

class EditarPedidoSchema(BaseModel):
    cliente_fk : int
    status : str
    periodo : str
    itens: List[ItemPedido]

