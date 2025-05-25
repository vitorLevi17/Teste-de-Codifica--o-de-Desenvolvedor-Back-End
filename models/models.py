from sqlalchemy import Column, Integer, String,DECIMAL,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    descricao=Column(String)
    valor_venda=Column(DECIMAL)
    cd_barra=Column(String)
    secao=Column(String)
    estoque_inicial=Column(Integer)
    dt_validade=Column(String)
    imagem=Column(String)
    disponivel_s_n=Column(String)

class Pedidos(Base):
    __tablename__ = 'pedidos'

    id=Column(Integer,primary_key=True,index=True)
    cliente_fk=Column(Integer,ForeignKey('clientes.id'))
    produto_fk=Column(Integer,ForeignKey('produtos.id'))
    quantidade_itens = Column(Integer)
    status = Column(String)
    periodo = Column(String)

    cliente = relationship("Cliente")
    produto = relationship("Produtos")

class Users(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String,nullable=False,unique=True)
    senha = Column(String,nullable=False)
    nivel = Column(String,nullable=False) #admin / regular

