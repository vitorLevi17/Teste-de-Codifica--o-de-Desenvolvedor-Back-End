from pydantic import BaseModel
from decimal import Decimal
""" 
    Schema para produtos e sua exibição em pedidos
"""
#Para exibir produtos
class ProdutoSchema(BaseModel):
    id : int
    nome_produto : str
    categoria : str
    preco : float
    descricao : str
    valor_venda : float
    cd_barra : str
    secao : str
    estoque : int
    dt_validade : str
    imagem : str
    disponivel_s_n : str

#Para criação e exibição de pedido
class ProdutoSchemaPedido(BaseModel):
    nome_produto : str
    categoria : str
    preco : float
    descricao : str
    secao : str
    imagem : str

#Schema para criar produto
class ProdutoCriarSchema(BaseModel):
    nome_produto : str
    categoria : str
    preco : Decimal
    descricao : str
    valor_venda : Decimal
    cd_barra : str
    secao : str
    estoque : int
    dt_validade : str
    imagem : str
    disponivel_s_n : str
