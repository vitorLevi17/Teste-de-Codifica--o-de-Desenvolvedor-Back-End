from fastapi import FastAPI
from routers import cliente, produto
from models.database import engine
from models.models import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(cliente.router,prefix='/cliente',tags=['Clientes'])
app.include_router(produto.router,prefix='/produto',tags=['Produtos'])

@app.get('/')
def index():
    return "hello world"




