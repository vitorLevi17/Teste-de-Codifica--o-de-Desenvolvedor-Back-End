from pydantic import BaseModel
"""
    Schemas relacionados aos clientes e sua exibição no endpoint de pedidos
"""
#Schema para exibir clientes
class ClienteSchema(BaseModel):
    id: int
    nome: str
    telefone: str
    email: str
    cpf: str
#Schema para exibir no cliente no endpoint pedido
class ClienteSchemaPedido(BaseModel):
    nome: str
    telefone: str
    email: str
#Schema para criar o cliente
class ClienteCriarSchema(BaseModel):
    nome: str
    telefone: str
    email: str
    cpf: str

    class Config:
        orm_mode = True