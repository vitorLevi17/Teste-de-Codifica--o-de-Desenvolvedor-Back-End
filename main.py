from fastapi import FastAPI
from routers import cliente, produto,pedidos,usuarios
from models.database import engine
from models.models import Base
app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(cliente.router,prefix='/cliente',tags=['Clientes'])
app.include_router(produto.router,prefix='/produto',tags=['Produtos'])
app.include_router(pedidos.router,prefix='/pedidos',tags=['Pedidos'])
#app.include_router(usuarios.router,prefix='/usuarios',tags=['Usuarios'])

@app.get('/')
def index():
    return "hello world"