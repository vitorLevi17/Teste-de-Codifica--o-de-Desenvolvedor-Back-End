from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()
class Clientes(BaseModel):
    id:int
    nome:str
    telefone:str
    email:str
    cpf:str

clientes_db = []

@router.get('/',response_model=List[Clientes])
def cliente():
    return clientes_db

@router.post('/',response_model=Clientes)
def criar_cliente(cliente: Clientes):
    clientes_db.append(cliente)
    return True