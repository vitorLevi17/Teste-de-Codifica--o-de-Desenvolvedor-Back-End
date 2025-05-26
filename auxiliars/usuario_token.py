from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import models
from models.database import SessionLocal

"""
    Arquivo para auxiliar o endpoint de usuarios a identificar o usuario atravez do token
"""

#Variaveis de ambiente da aplicação
SECRET_KEY = "secreto-superseguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Metodo que possibilita ações no banco de dados, abrindo a sessão local
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Schema oauth2 para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#Como parametro, o metodo necessita do token e da sessao do banco
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    #Exceção que será usada abaixo
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    #email equivale ao nome de acesso
    #Se o nome não existir, a exceção é lançada e o acesso negado
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    #Buscar usuario pelo nome para verificar se ele está cadastrado no sistema
    user = db.query(models.Users).filter(models.Users.nome == email).first()
    if user is None:
        raise credentials_exception
    return user

#Esse metodo segue a mesma logica do metodo anterior, contudo, ele serve para restringir o acesso ao endpoint de registro de usuarios, sendo visivel apenas para admins
def get_current_user_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Você não está autorizado a acessar esse endpoint",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.Users).filter(models.Users.nome == email).first()
    #Aqui está a restrição de usuarios regulares
    if user is None or user.nivel != "admin":
        raise credentials_exception
    return user