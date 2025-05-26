from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Caminho usado para o banco de dados SQLite, no caso, armazenado dentro da aplicação
DATABASE_URL = "sqlite:///./banco.db"

#Criação do banco na aplicação
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
