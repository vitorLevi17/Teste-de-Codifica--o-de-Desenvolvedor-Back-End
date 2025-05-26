from typing import List
from fastapi import APIRouter, Depends, Query
from auxiliars import validacoes
from sqlalchemy.orm import Session
from models import models
from models.database import SessionLocal
from schemas.cliente import ClienteSchema,ClienteCriarSchema
from auxiliars.usuario_token import get_current_user
"""
    Endpoint para gerenciar os clientes da aplicação.
    
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

#Metodo para listar clientes
#Parametros(limite de registros por pagina
#           filtro do nome
#           filtro do email

@router.get('/',response_model=List[ClienteSchema])
def cliente(db: Session = Depends(get_db),skip: int = Query(0, ge=0),
            limit: int = Query(10, le=100),
            nome: str = Query(None),
            email: str = Query(None),
            current_user: models.Users = Depends(get_current_user)
            ):
    #Acessar banco
    query = db.query(models.Cliente)

    #Se o filtro escolhido for o de nome, a variavel query busca pelo nome passado
    if nome:
        query = query.filter(models.Cliente.nome.ilike(f"%{nome}%"))

    # Se o filtro escolhido for o de email, a variavel query busca pelo email informado
    if email:
        query = query.filter(models.Cliente.email.ilike(f"%{email}%"))

    #Retornar valores com paginação e filtros
    clientes = query.offset(skip).limit(limit).all()
    return clientes

#Buscar cliente por id especifico
#Recebe o id para identificar o cliente
@router.get('/{cliente_id}',response_model=ClienteSchema)
def cliente_id(cliente_id:int, db: SessionLocal = Depends(get_db),
               current_user: models.Users = Depends(get_current_user)):

    #Buscar cliente pelo id
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    #Metodo pra validar o cliente pelo id, caso o metodo não encontre o cliente, retorna a mesngem de erro
    validacoes.validar_objeto_bd(cliente,cliente_id)
    return cliente

#Criar cliente
@router.post('/',response_model=ClienteSchema)
def criar_cliente(cliente: ClienteCriarSchema, db: Session = Depends(get_db),
                  current_user: models.Users = Depends(get_current_user)):
    # Recebe os objetos do cliente
    cliente_novo = models.Cliente(**cliente.dict())

    #Validações das informações do novo cliente
    validacoes.validar_cliente(cliente_novo,db)

    #Adicionar ao banco de dados
    db.add(cliente_novo)

    #Commitar as alterções
    db.commit()
    #Recarregar o banco para exibir as informações
    db.refresh(cliente_novo)

    return cliente_novo

#Editar Cliente
@router.put('/{cliente_id}',response_model=ClienteSchema)
def editar_cliente(cliente_id: int,cliente_put: ClienteCriarSchema, db:Session = Depends(get_db),
                   current_user: models.Users = Depends(get_current_user)):
    # Buscar cliente pelo id
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    # Metodo pra validar se o cliente existe, pelo id
    validacoes.validar_objeto_bd(cliente,cliente_id)

    #Receber dados atualizados
    cliente_dados_atualizados = cliente_put

    #Validar dados atualizados
    validacoes.validar_cliente_editar(cliente_dados_atualizados, db, cliente_id=cliente_id)

    #Passar pelos pares chave e valor do json para conferir as alterações
    for key, value in cliente_put.dict().items():
        setattr(cliente,key,value)

    #Comitar alterações
    db.commit()
    db.refresh(cliente)
    return cliente

#Metodo de deleção de clientes
@router.delete('/{cliente_id}')
def excluir_cliente(cliente_id: int, db: Session = Depends(get_db),
                    current_user: models.Users = Depends(get_current_user)):

    # Buscar cliente pelo id
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    #Validar se o cliente existe
    validacoes.validar_objeto_bd(cliente, cliente_id)

    #Apagar cliente
    db.delete(cliente)

    #Commitar alteração
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso"}