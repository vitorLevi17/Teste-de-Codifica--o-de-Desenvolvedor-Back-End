from pydantic import BaseModel

class ClienteSchema(BaseModel):
    id: int
    nome: str
    telefone: str
    email: str
    cpf: str

class ClienteCriarSchema(BaseModel):
    nome: str
    telefone: str
    email: str
    cpf: str

    class Config:
        orm_mode = True