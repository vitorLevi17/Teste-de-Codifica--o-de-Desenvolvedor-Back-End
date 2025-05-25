from fastapi import HTTPException, status
from validate_docbr import CPF
from models import models
import re
from datetime import datetime
def validar_objeto_bd(objeto,objeto_id):
    if objeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {objeto_id} não encontrado"
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
def validar_produto(produto,db):
    padrao_dt = r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
    padrao_img = r'^[\w\.-]+\.(png|jpg|jpeg|)$'

    if db.query(models.Produtos).filter(models.Produtos.nome_produto == produto.nome_produto).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O Nome do produto já está cadastrado."
        )
    if produto.preco <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O preço do produto deve ser maior ou igual que 0."
        )
    if produto.valor_venda >= produto.preco:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O produto deve ser vendido com preço maior do que foi comprado."
        )
    if db.query(models.Produtos).filter(models.Produtos.cd_barra == produto.cd_barra).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Codigo de barras já cadastrado."
        )
    if produto.estoque_inicial <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O numero de itens do estoque deve ser maior ou igual a 1."
        )
    if not re.match(padrao_dt,produto.dt_validade):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A data de validade ter formato dd/mm/yyyy."
        )
    dt_validade = datetime.strptime(produto.dt_validade,"%d/%m/%Y")
    if dt_validade <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A data de validade deve ser maior que a data atual."
        )
    if not re.match(padrao_img,produto.imagem):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O formato da imagem deve ser jpeg ou png."
        )
