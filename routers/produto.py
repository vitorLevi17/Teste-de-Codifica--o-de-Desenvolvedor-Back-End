from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.database import SessionLocal
from sqlalchemy.orm import Session
from models import models
from typing import List
from schemas.produto import ProdutoSchema,ProdutoCriarSchema
from auxiliars import validacoes
from auxiliars.usuario_token import get_current_user

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get('/',response_model=List[ProdutoSchema])
def produto(db: SessionLocal = Depends(get_db),skip: int = Query(0, ge=0),
    limit: int = Query(10,le=100),
    categoria: str = Query(None),
    preco: float = Query(None),
    disponivel_s_n: str = Query(None),
    current_user: models.Users = Depends(get_current_user)
            ):
    query = db.query(models.Produtos)

    if categoria:
        query = query.filter(models.Produtos.categoria.ilike(f"%{categoria}%"))
    if preco:
        query = query.filter(models.Produtos.preco.ilike(f"%{preco}%"))
    if disponivel_s_n:
        query = query.filter(models.Produtos.disponivel_s_n.ilike(f"%{disponivel_s_n}%"))

    produtos = query.offset(skip).limit(limit).all()
    return produtos

@router.get('/{produto_id}',response_model=ProdutoSchema)
def produto_id(produto_id:int ,db: SessionLocal = Depends(get_db),
               current_user: models.Users = Depends(get_current_user)):
    produto = db.query(models.Produtos).filter(models.Produtos.id == produto_id).first()
    validacoes.validar_objeto_bd(produto,produto_id)
    return produto
@router.post('/',response_model=ProdutoSchema)
def criar_produto(produto: ProdutoCriarSchema,db:Session = Depends(get_db),
                  current_user: models.Users = Depends(get_current_user)):
    produto_novo = models.Produtos(**produto.dict())
    validacoes.validar_produto(produto, db)
    db.add(produto_novo)
    db.commit()
    db.refresh(produto_novo)
    return produto_novo
@router.put('/{produto_id}',response_model=ProdutoSchema)
def editar_produto(produto_id:int,produto_put:ProdutoCriarSchema,db:Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    produto = db.query(models.Produtos).filter(models.Produtos.id == produto_id).first()

    validacoes.validar_objeto_bd(produto,produto_id)
    produto_atualizado = produto_put
    validacoes.validar_produto_editar(produto_atualizado,db,produto_id)

    for key, value in produto_put.dict().items():
        setattr(produto,key,value)

    db.commit()
    db.refresh(produto)
    return produto
@router.delete('/{produto_id}')
def excluir_produto(produto_id: int, db:Session = Depends(get_db),
                    current_user: models.Users = Depends(get_current_user)):
    produto = db.query(models.Produtos).filter(models.Produtos.id == produto_id).first()
    validacoes.validar_objeto_bd(produto,produto_id)
    db.delete(produto)
    db.commit()
    return {"mensagem": "Produto deletado com sucesso"}