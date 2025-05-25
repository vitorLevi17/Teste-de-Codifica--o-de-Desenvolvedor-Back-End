from typing import List
from pydantic import BaseModel

class ItemPedido(BaseModel):
    produto_id : int
    quantidade : int
class PedidoSchema(BaseModel):
    id : int
    cliente_fk : int
    status : str
    periodo : str
    itens: List[ItemPedido]

class CriarPedidoSchema(BaseModel):
    cliente_fk : int
    periodo : str
    itens: List[ItemPedido]

class EditarPedidoSchema(BaseModel):
    cliente_fk : int
    produto_fk : int
    status : str
    periodo : str

