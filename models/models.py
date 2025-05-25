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
    estoque=Column(Integer)
    dt_validade=Column(String)
    imagem=Column(String)
    disponivel_s_n=Column(String)

class Pedidos(Base):
    __tablename__ = 'pedidos'

    id=Column(Integer,primary_key=True,index=True)
    cliente_fk=Column(Integer,ForeignKey('clientes.id'))
    #produto_fk=Column(Integer,ForeignKey('produtos.id'))
    status = Column(String)
    periodo = Column(String)

    cliente = relationship("Cliente")
    itens = relationship("Item_Pedido", back_populates="pedido")

class Item_Pedido(Base):
    __tablename__ = 'itens_pedidos'

    id=Column(Integer,primary_key=True,index=True)
    pedido_fk=Column(Integer,ForeignKey('pedidos.id'))
    produto_id_fk = Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer)

    pedido = relationship("Pedidos", back_populates="itens")
    produto = relationship("Produtos")
class Users(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String,nullable=False,unique=True)
    senha = Column(String,nullable=False)
    nivel = Column(String,nullable=False) #admin / regular

