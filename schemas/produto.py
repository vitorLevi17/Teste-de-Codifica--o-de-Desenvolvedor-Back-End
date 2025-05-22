from datetime import date
from pydantic import BaseModel
from decimal import Decimal


class ProdutoSchema(BaseModel):
    id : int
    nome_produto : str
    categoria : str
    preco : float
    disponivel : bool
    descricao : str
    valor_venda : float
    cd_barra : str
    secao : str
    estoque_inicial : int
    dt_validade : str
    imagem : str

class ProdutoCriarSchema(BaseModel):
    nome_produto : str
    categoria : str
    preco : Decimal
    disponivel : bool
    descricao : str
    valor_venda : Decimal
    cd_barra : str
    secao : str
    estoque_inicial : int
    dt_validade : str
    imagem : str
