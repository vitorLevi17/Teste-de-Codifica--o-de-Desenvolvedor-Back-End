from fastapi import FastAPI
from routers import cliente

app = FastAPI()
app.include_router(cliente.router,prefix='/cliente',tags=['Clientes'])

@app.get('/')
def index():
    return "hello world"




