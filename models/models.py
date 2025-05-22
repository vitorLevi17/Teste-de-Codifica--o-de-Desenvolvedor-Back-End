from sqlalchemy import Column, Integer, String,DECIMAL,Boolean,Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    telefone = Column(String)
    email = Column(String)
    cpf = Column(String)

class Produtos(Base):
    __tablename__ = 'produtos'

    id=Column(Integer,primary_key=True,index=True)
    nome_produto=Column(String)
    categoria=Column(String)
    preco=Column(DECIMAL)
    disponivel=Column(Boolean)
    descricao=Column(String)
    valor_venda=Column(DECIMAL)
    cd_barra=Column(String)
    secao=Column(String)
    estoque_inicial=Column(Integer)
    dt_validade=Column(String)
    imagem=Column(String)
