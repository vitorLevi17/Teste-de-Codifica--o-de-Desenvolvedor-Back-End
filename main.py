from fastapi import FastAPI, Depends

from models import models
from routers import cliente, produto,pedidos,usuarios
from models.database import engine
from models.models import Base
from auxiliars.usuario_token import get_current_user
app = FastAPI()
Base.metadata.create_all(bind=engine)

#Registrar as urls dos endpoints
app.include_router(cliente.router,prefix='/clients',tags=['Clientes'])
app.include_router(produto.router,prefix='/products',tags=['Produtos'])
app.include_router(pedidos.router,prefix='/orders',tags=['Pedidos'])
app.include_router(usuarios.router,prefix='/auth',tags=['Usuarios'])

@app.get('/')
def index(current_user: models.Users = Depends(get_current_user)):
    endpoints = [
        #Exibir para o usuario as listas de rotas disponiveis
        '127.0.0.1:8000/clients',
        '127.0.0.1:8000/products',
        '127.0.0.1:8000/orders',
        '127.0.0.1:8000/auth'
    ]
    return endpoints