from fastapi import HTTPException, status
from validate_docbr import CPF
from models import models
import re

def validar_objeto_bd(objeto,objeto_id):
    if objeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {objeto_id} não encontrado"
        )
def validar_cliente(cliente,db):
    valida_cpf = CPF()
    padrao_telefone = '[0-9]{2} [0-9]{5}-[0-9]{4}'
    padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if db.query(models.Cliente).filter(models.Cliente.nome == cliente.nome).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nome já está cadastrado."
        )

    if db.query(models.Cliente).filter(models.Cliente.email == cliente.email).first() or not re.match(padrao_email,cliente.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"email inválido ou já cadastrado."
        )

    if not valida_cpf.validate(cliente.cpf) or db.query(models.Cliente).filter(models.Cliente.cpf == cliente.cpf).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O CPF do cliente é inválido ou já está cadastrado."
        )

    if re.findall(cliente.telefone,padrao_telefone) or db.query(models.Cliente).filter(models.Cliente.telefone == cliente.telefone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Telefone já está cadastrado ou é inválido."
        )

def validar_cliente_editar(cliente, db, cliente_id=None):
    valida_cpf = CPF()
    padrao_telefone = r'^[0-9]{2} [0-9]{5}-[0-9]{4}$'
    padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if db.query(models.Cliente).filter(models.Cliente.nome == cliente.nome, models.Cliente.id != cliente_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome já está cadastrado."
        )
    if db.query(models.Cliente).filter(models.Cliente.email == cliente.email, models.Cliente.id != cliente_id).first() or not re.match(padrao_email, cliente.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail inválido ou já cadastrado."
        )
    if db.query(models.Cliente).filter(models.Cliente.cpf == cliente.cpf, models.Cliente.id != cliente_id).first() or not valida_cpf.validate(cliente.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF inválido ou já cadastrado."
        )
    if db.query(models.Cliente).filter(models.Cliente.telefone == cliente.telefone, models.Cliente.id != cliente_id).first() or not re.match(padrao_telefone, cliente.telefone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telefone inválido ou já cadastrado."
        )