from fastapi import APIRouter,Depends
from models.database import SessionLocal
from sqlalchemy.orm import Session
from models import models
from typing import List
from schemas.produto import ProdutoSchema,ProdutoCriarSchema

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

@router.post('/',response_model=ProdutoSchema)
def criar_produto(produto: ProdutoCriarSchema,db:Session = Depends(get_db)):
    produto_novo = models.Produtos(**produto.dict())
    db.add(produto_novo)
    db.commit()
    db.refresh(produto_novo)
    return produto_novo