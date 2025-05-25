from pydantic import BaseModel
from decimal import Decimal
class ProdutoSchema(BaseModel):
    id : int
    nome_produto : str
    categoria : str
    preco : float
    descricao : str
    valor_venda : float
    cd_barra : str
    secao : str
    estoque_inicial : int
    dt_validade : str
    imagem : str
    disponivel_s_n : str

class ProdutoCriarSchema(BaseModel):
    nome_produto : str
    categoria : str
    preco : Decimal
    descricao : str
    valor_venda : Decimal
    cd_barra : str
    secao : str
    estoque_inicial : int
    dt_validade : str
    imagem : str
    disponivel_s_n : str
