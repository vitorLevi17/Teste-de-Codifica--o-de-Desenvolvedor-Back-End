from typing import List
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from models import models
from models.models import Pedidos, Produtos, Item_Pedido, Cliente
from schemas.pedidos import PedidoSchemaList,CriarPedidoSchema,EditarPedidoSchema,PedidoSchema
from models.database import SessionLocal
from auxiliars import validacoes
from auxiliars import validacoes_pedidos
from auxiliars.usuario_token import get_current_user

"""
    Endpoint para gerenciar os pedidos da aplicação
    
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

#Metodo para listar pedidos e seus produtos/clientes
#Parametros(limite de registros por pagina
#           filtro por status
#           filtro por periodos
#           filtro por id_cliente
@router.get('/',response_model=List[PedidoSchemaList])
def pedidos(db:SessionLocal = Depends(get_db),skip: int = Query(0, ge=0),
            limit: int = Query(10,le=100),
            periodo: str=Query(None),
            status: str=Query(None),
            id_cliente: int=Query(None),
            current_user: models.Users = Depends(get_current_user)):

    # Acessar banco
    query_pedidos = db.query(models.Pedidos)

    # Se o filtro escolhido for o de periodo, a variavel query busca pelos pedidos com o periodo que foi passado
    if periodo:
        query_pedidos = query_pedidos.filter(models.Pedidos.periodo.ilike(f"%{periodo}%"))

    # Se o filtro escolhido for o de id do cliente, a variavel query busca pelos pedidos do id do cliente que foi passado
    if id_cliente:
        query_pedidos = query_pedidos.filter(Pedidos.cliente_fk == id_cliente)

    # Se o filtro escolhido for o de status, a variavel query busca pelos pedidos do status que foi passado
    if status:
        query_pedidos = query_pedidos.filter(models.Pedidos.status.ilike(f"%{status}%"))

    #Pegar todos os pedidos
    query = query_pedidos.offset(skip).limit(limit)
    pedidos = query.all()

    #Criar lista que será preenchida para exibir todas as informações do pedido pro usuario
    resultado = []

    for pedido in pedidos:

        #Pegar itens do pedido
        itens = db.query(Item_Pedido).filter(Item_Pedido.pedido_fk == pedido.id).all()

        #Pegar produtos dos itens
        produtos = db.query(Produtos).join(Item_Pedido).filter(Item_Pedido.pedido_fk == pedido.id).all()

        #Pegar cliente do pedido
        cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_fk).first()

        #Adicionar valores a lista resultado
        resultado.append({
            "id": pedido.id,
            "cliente_fk": pedido.cliente_fk,
            "status": pedido.status,
            "periodo": pedido.periodo,
            "itens": [{"produto_id": item.produto_id_fk, "quantidade": item.quantidade}for item in itens],
            "produto": [{"nome_produto": produto.nome_produto,"categoria": produto.categoria,
                     "preco": produto.preco,"descricao": produto.descricao,
                     "secao": produto.secao,"imagem": produto.imagem} for produto in produtos],
             "cliente":{"nome": cliente.nome,"telefone": cliente.telefone,"email":cliente.email},
    })
    return resultado

#Buscar pedido por id especifico
#Recebe o id para identificar o pedido
@router.get('/{pedidos_id}',response_model=PedidoSchemaList)
def pedido_id(pedidos_id:int ,db:SessionLocal = Depends(get_db),
              current_user: models.Users = Depends(get_current_user)):
    # Buscar pedido pelo id
    pedido = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()

    # Metodo pra validar o cliente pelo id, caso o metodo não encontre o cliente, retorna a mesngem de erro
    validacoes.validar_objeto_bd(pedido, pedidos_id)

    # Pegar itens do pedido
    produtos = db.query(Produtos).join(Item_Pedido).filter(Item_Pedido.pedido_fk == pedidos_id).all()

    # Pegar cliente do pedido
    cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_fk).first()

    # Pegar produtos dos itens
    itens = db.query(Item_Pedido).filter(Item_Pedido.pedido_fk == pedidos_id).all()

    #Retornar pedido especifico
    pedido_completo = {
        "id": pedido.id,
        "cliente_fk": pedido.cliente_fk,
        "status": pedido.status,
        "periodo": pedido.periodo,
        "itens": [{"produto_id": item.produto_id_fk, "quantidade": item.quantidade}for item in itens],
        "produto": [{"nome_produto": produto.nome_produto, "categoria": produto.categoria,
                     "preco": produto.preco, "descricao": produto.descricao,
                     "secao": produto.secao, "imagem": produto.imagem} for produto in produtos],
        "cliente": {"nome": cliente.nome, "telefone": cliente.telefone, "email": cliente.email},
    }
    return pedido_completo

#Criar pedido
@router.post('/')
def criar_pedido(pedidos: CriarPedidoSchema,db:SessionLocal = Depends(get_db),
                 current_user: models.Users = Depends(get_current_user)):

    #Validar valores recebidos
    validacoes_pedidos.validar_pedido(pedidos,db)

    #Criar pedido
    pedido_post = Pedidos(cliente_fk = pedidos.cliente_fk,
                          status="Em preparação",
                          periodo=pedidos.periodo)

    #Adicionar pedido na tabela do bd
    db.add(pedido_post)
    db.commit()
    db.refresh(pedido_post)

    #Adicionar item na tabela do bd
    for item in pedidos.itens:
        item_pedido = Item_Pedido(
            pedido_fk = pedido_post.id,
            produto_id_fk = item.produto_id,
            quantidade = item.quantidade
        )
        db.add(item_pedido)

        #Reduzir o estoque do produto
        produto = db.query(Produtos).filter(Produtos.id == item.produto_id).first()
        produto.estoque -= item.quantidade

    db.commit()
    return {"message": "Pedido criado com sucesso", "pedido_id": pedido_post.id}

@router.put('/{pedidos_id}', response_model=PedidoSchema)
def editar_pedido(pedidos_id: int, pedido_put: EditarPedidoSchema, db: Session = Depends(get_db),
                  current_user: models.Users = Depends(get_current_user)):

    # Buscar pedido pelo id
    pedido = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()

    # Metodo pra validar se o pedido existe, pelo id
    validacoes.validar_objeto_bd(pedido, pedidos_id)

    #Validar dados atualizados
    validacoes_pedidos.validar_pedido(pedido_put,db)
    pedido.cliente_fk = pedido_put.cliente_fk
    pedido.status = pedido_put.status
    pedido.periodo = pedido_put.periodo

    #Deletar os dados que foram removidos
    db.query(models.Item_Pedido).filter(models.Item_Pedido.pedido_fk == pedidos_id).delete()

    #Atualizar itens
    for item in pedido_put.itens:
        novo_item = models.Item_Pedido(
            pedido_fk=pedidos_id,
            produto_id_fk=item.produto_id,
            quantidade=item.quantidade
        )
        #Adicionar item
        db.add(novo_item)

    db.commit()
    db.refresh(pedido)
    return pedido
@router.delete('/{pedidos_id}')
def excluir_pedido(pedidos_id: int, db: Session = Depends(get_db),
                   current_user: models.Users = Depends(get_current_user)):

    # Buscar pedido pelo id
    pedidos = db.query(models.Pedidos).filter(models.Pedidos.id == pedidos_id).first()

    # Validar se o pedido existe
    validacoes.validar_objeto_bd(pedidos,pedidos_id)

    #Deletar itens
    itens = db.query(Item_Pedido).filter(Item_Pedido.pedido_fk == pedidos_id).all()
    for item in itens:
        db.delete(item)
    db.delete(pedidos)

    #Commitar
    db.commit()
    return {"mensagem":"Pedido deletado com sucesso"}