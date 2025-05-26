from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.database import SessionLocal
from sqlalchemy.orm import Session
from models import models
from typing import List
from schemas.produto import ProdutoSchema,ProdutoCriarSchema
from auxiliars import validacoes
from auxiliars.usuario_token import get_current_user
"""
    Endpoint para gerenciamento de produtos
    
    Visivel para todos os usuarios logados da api.
    
    Parametros padrões para essas rotas (db: Session = Depends(get_db) = sessão do banco de dados,
     current_user: models.Users = Depends(get_current_user) metodo de proteção do endpoint para usuarios logados)
"""
router = APIRouter()

#Metodo para fazer operações em banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Metodo para listar clientes
# Parametros(limite de registros por pagina
# filtro da categoria
# filtro do preco
# filtro do preco
# filtro da disponibilidade do produto
@router.get('/',response_model=List[ProdutoSchema])
def produto(db: SessionLocal = Depends(get_db),skip: int = Query(0, ge=0),
    limit: int = Query(10,le=100),
    categoria: str = Query(None),
    preco: float = Query(None),
    disponivel_s_n: str = Query(None),
    current_user: models.Users = Depends(get_current_user)
            ):
    # Acessar banco
    query = db.query(models.Produtos)

    # Se o filtro escolhido for o de categoria, a variavel query busca pela categoria passada
    if categoria:
        query = query.filter(models.Produtos.categoria.ilike(f"%{categoria}%"))

    # Se o filtro escolhido for o de preço, a variavel query busca pelo preço passado
    if preco:
        query = query.filter(models.Produtos.preco.ilike(f"%{preco}%"))

    # Se o filtro escolhido for o de disponivel_s_n, a variavel query busca pelo disponivel_s_n passado
    if disponivel_s_n:
        query = query.filter(models.Produtos.disponivel_s_n.ilike(f"%{disponivel_s_n}%"))

    # Retornar valores com paginação e filtros
    produtos = query.offset(skip).limit(limit).all()
    return produtos

#Buscar produto por id especifico
#Recebe o id para identificar o produto
@router.get('/{produto_id}',response_model=ProdutoSchema)
def produto_id(produto_id:int ,db: SessionLocal = Depends(get_db),
               current_user: models.Users = Depends(get_current_user)):
    # Buscar produto pelo id
    produto = db.query(models.Produtos).filter(models.Produtos.id == produto_id).first()

    # Metodo pra validar o cliente pelo id, caso o metodo não encontre o cliente, retorna a mesngem de erro
    validacoes.validar_objeto_bd(produto,produto_id)
    return produto

#Criar produto
@router.post('/',response_model=ProdutoSchema)
def criar_produto(produto: ProdutoCriarSchema,db:Session = Depends(get_db),
                  current_user: models.Users = Depends(get_current_user)):
    # Recebe os objetos do produto
    produto_novo = models.Produtos(**produto.dict())

    # Validações das informações do novo produto
    validacoes.validar_produto(produto, db)

    # Adicionar ao banco de dados
    db.add(produto_novo)

    # Commitar as alterções
    db.commit()

    # Recarregar o banco para exibir as informações
    db.refresh(produto_novo)

    return produto_novo
@router.put('/{produto_id}',response_model=ProdutoSchema)
def editar_produto(produto_id:int,produto_put:ProdutoCriarSchema,db:Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    # Buscar produto pelo id
    produto = db.query(models.Produtos).filter(models.Produtos.id == produto_id).first()

    #Metodo pra validar se o produto existe, pelo id
    validacoes.validar_objeto_bd(produto,produto_id)

    # Receber dados atualizados
    produto_atualizado = produto_put

    # Validar dados atualizados
    validacoes.validar_produto_editar(produto_atualizado,db,produto_id)

    # Passar pelos pares chave e valor do json para conferir as alterações
    for key, value in produto_put.dict().items():
        setattr(produto,key,value)

    # Comitar alterações
    db.commit()
    db.refresh(produto)
    return produto

#Metodo de deleção de clientes
@router.delete('/{produto_id}')
def excluir_produto(produto_id: int, db:Session = Depends(get_db),
                    current_user: models.Users = Depends(get_current_user)):
    # Buscar produto pelo id
    produto = db.query(models.Produtos).filter(models.Produtos.id == produto_id).first()

    # Validar se o cliente existe
    validacoes.validar_objeto_bd(produto,produto_id)

    # Apagar cliente
    db.delete(produto)
    db.commit()
    return {"mensagem": "Produto deletado com sucesso"}