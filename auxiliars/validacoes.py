from fastapi import HTTPException, status
from validate_docbr import CPF
from models import models
import re
from datetime import datetime
"""Validações de objetos de rotas de criação e ediçao"""

#Metodo para validar se os objetos requisitados existem no banco, caso a exceção seja lançada, os objetos não existem e a execução para
def validar_objeto_bd(objeto,objeto_id):
    #Se não existir, lança a exceção
    if objeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {objeto_id} não foi encontrado"
        )

#Metodo com as validações do cliente
def validar_cliente(cliente,db):
    #Importar lib de validação de documentos brasileiros
    valida_cpf = CPF()
    #Padrão para telefones
    padrao_telefone = '[0-9]{2} [0-9]{5}-[0-9]{4}'
    #Padrão para emails
    padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    #Validar se o nome do cliente já está cadaastrado no sistema, verificando se já existe no banco e lançando a exceção
    if db.query(models.Cliente).filter(models.Cliente.nome == cliente.nome).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nome já está cadastrado."
        )
    # Validar se o email do cliente já está cadaastrado no sistema, verificando se já existe no banco, verificando se a strnig segue o padrão especificado e lançando a exceção caso sim
    if db.query(models.Cliente).filter(models.Cliente.email == cliente.email).first() or not re.match(padrao_email,cliente.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"email inválido ou já cadastrado."
        )
    # Validar se o cpf do cliente já está cadastrado no sistema, verificando se já existe no banco, usando o metodo validate da lib doc-br e lançando a exceção caso sim
    if not valida_cpf.validate(cliente.cpf) or db.query(models.Cliente).filter(models.Cliente.cpf == cliente.cpf).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O CPF do cliente é inválido ou já está cadastrado."
        )
    # Validar se o telefone do cliente já está cadaastrado no sistema, verificando se já existe no banco, verificando se a strnig segue o padrão especificado e lançando a exceção caso sim
    if re.findall(cliente.telefone,padrao_telefone) or db.query(models.Cliente).filter(models.Cliente.telefone == cliente.telefone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Telefone já está cadastrado ou é inválido."
        )
#Para esse metodo, segue a mesma logica do metodo anterior, porem, filtrando pelo id para que não caia nas validações de duplicidade
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

#Validar a criação dos produtos
def validar_produto(produto,db):
    #padrão de data que deve ser seguido
    padrao_dt = r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
    # padrão de imagem que deve ser seguido
    padrao_img = r'^[\w\.-]+\.(png|jpg|jpeg|)$'
    # Validar se o nome do produto já está cadastrado no sistema, verificando se já existe no banco e lançando a exceção
    if db.query(models.Produtos).filter(models.Produtos.nome_produto == produto.nome_produto).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O Nome do produto já está cadastrado."
        )
    # Validar se o preco do produto é maior ou igual a 0, ele n pode ser comercializado com valor 0
    if produto.preco <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O preço do produto deve ser maior ou igual que 0."
        )
    # Validar se o preco do produto é maior que o valor que foi adquirido pela empresa para ser comercializado
    if produto.valor_venda >= produto.preco:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O produto deve ser vendido com preço maior do que foi comprado."
        )
    #Validar unicidade do codigo de barras
    if db.query(models.Produtos).filter(models.Produtos.cd_barra == produto.cd_barra).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Codigo de barras já cadastrado."
        )
    #Se o estoque for menor que 0, o produto n pode ser comercializado
    if produto.estoque <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O numero de itens do estoque deve ser maior ou igual a 1."
        )
    #Conferir padrão da data,caso não esteja no padrão, a excessão é lançada
    if not re.match(padrao_dt,produto.dt_validade):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A data de validade ter formato dd/mm/yyyy."
        )
    #Checar se a data de validade é maior que o dia presente
    dt_validade = datetime.strptime(produto.dt_validade,"%d/%m/%Y")
    if dt_validade <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A data de validade deve ser maior que a data atual."
        )
    #Conferir se o tipo de imagem é valido, os tipos validos estão presentes na lista
    if not re.match(padrao_img,produto.imagem):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O formato da imagem deve ser jpeg ou png."
        )
    #Esse campo só pode receber sim ou não para disponibilidade
    if produto.disponivel_s_n not in ["Sim","Não"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"As respostas disponiveis para esse campo são 'Sim' ou 'Não'."
        )
#Esse metodo segue a mesma logica do metodo acima, porem, checando o id para que a duplicidade não seja confundida
def validar_produto_editar(produto,db, produto_id=None):
    padrao_dt = r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
    padrao_img = r'^[\w\.-]+\.(png|jpg|jpeg|)$'

    if db.query(models.Produtos).filter(models.Produtos.nome_produto == produto.nome_produto,models.Produtos.id != produto_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O Nome do produto já está cadastrado."
        )
    if produto.preco <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O preço do produto deve ser maior que 0."
        )
    if produto.valor_venda >= produto.preco:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O produto deve ser vendido com preço maior do que foi comprado."
        )
    if db.query(models.Produtos).filter(models.Produtos.cd_barra == produto.cd_barra, models.Produtos.id != produto_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Codigo de barras já cadastrado."
        )
    if produto.estoque < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O numero de itens do estoque deve ser maior que 1."
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
            detail=f"O formato da imagem deve ser jpeg,jpg ou png."
        )
    if produto.disponivel_s_n not in ["Sim","Não"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"As respostas disponiveis para esse campo são 'Sim' ou 'Não'."
        )