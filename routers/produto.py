from fastapi import APIRouter, Depends, HTTPException,status
from models.database import SessionLocal
from sqlalchemy.orm import Session
from models import models
from typing import List
from schemas.produto import ProdutoSchema,ProdutoCriarSchema
from auxiliars import validacoes

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/',response_model=List[ProdutoSchema])
def produto(db: SessionLocal = Depends(get_db)):
    produtos = db.query(models.Produtos).all()
    return produtos

@router.get('/{produto_id}',response_model=ProdutoSchema)
def produto_id(produto_id:int ,db: SessionLocal = Depends(get_db)):
    produto = db.query(models.Produtos).filter(models.Produtos.id == produto_id).first()
    validacoes.validar_objeto_bd(produto,produto_id)
    return produto

@router.post('/',response_model=ProdutoSchema)
def criar_produto(produto: ProdutoCriarSchema,db:Session = Depends(get_db)):
    produto_novo = models.Produtos(**produto.dict())
    validacoes.validar_produto(produto, db)
    db.add(produto_novo)
    db.commit()
    db.refresh(produto_novo)
    return produto_novo

@router.put('/{produto_id}',response_model=ProdutoSchema)
def editar_produto(produto_id:int,produto_put:ProdutoCriarSchema,db:Session = Depends(get_db)):
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
def excluir_produto(produto_id: int, db:Session = Depends(get_db)):
    produto = db.query(models.Produtos).filter(models.Produtos.id == produto_id).first()
    validacoes.validar_objeto_bd(produto,produto_id)
    db.delete(produto)
    db.commit()
    return {"mensagem": "Produto deletado com sucesso"}