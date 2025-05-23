from pydantic import BaseModel
class PedidoSchema(BaseModel):
    id : int
    cliente_fk : int
    produto_fk : int
    quantidade_itens : int
    status : str
    periodo : str

class CriarPedidoSchema(BaseModel):
    cliente_fk : int
    produto_fk : int
    quantidade_itens : int
    periodo : str

class EditarPedidoSchema(BaseModel):
    cliente_fk : int
    produto_fk : int
    quantidade_itens : int
    status : str
    periodo : str

