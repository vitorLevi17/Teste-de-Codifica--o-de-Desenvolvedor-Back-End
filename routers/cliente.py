from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import models
from models.database import SessionLocal
from schemas.cliente import ClienteSchema,ClienteCriarSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get('/',response_model=List[ClienteSchema])
def cliente(db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).all()
    return clientes

@router.post('/',response_model=ClienteSchema)
def criar_cliente(cliente: ClienteCriarSchema, db: Session = Depends(get_db)):
    cliente_novo = models.Cliente(**cliente.dict())
    db.add(cliente_novo)
    db.commit()
    db.refresh(cliente_novo)
    return cliente_novo