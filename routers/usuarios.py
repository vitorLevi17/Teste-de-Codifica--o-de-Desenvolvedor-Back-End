from datetime import datetime, timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import models
from models.database import SessionLocal
from schemas.usuarios import UsuarioSchema, Token
from auxiliars.usuario_token import get_current_user_admin
"""
    Rotas e metodos para gerir os usuarios
    
    Disponivel para todos os usuarios, menos o metodo de criar usuario que é limitado para os administradores
    
"""
router = APIRouter()

SECRET_KEY = "secreto-superseguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Senha encriptografada
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 padrão
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#Permitir operações em banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Criar o token de acesso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#Verificar senha encriptografa,e pegando do metodo get_password_hash
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#Pegar a senha encriptografada
def get_password_hash(password):
    return pwd_context.hash(password)

#Rota para usuario acessarem a API
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    #Verifica se o usuario está cadastrado
    user = db.query(models.Users).filter(models.Users.nome == form_data.username).first()
    if not user or not verify_password(form_data.password, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    #Usuario cadastro, é gerado um token de acesso a ele, durante seu uso na api
    token = create_access_token(data={"sub": user.nome})
    return {"access_token": token, "token_type": "bearer"}

#Metodo de registro de usuarios, limitado a admins
@router.post("/register", response_model=Token)
def register(user: UsuarioSchema, db: Session = Depends(get_db),
             current_user: models.Users = Depends(get_current_user_admin)):

    #Validar se já tem um usuario com esse nome no sistema
    existing = db.query(models.Users).filter(models.Users.nome == user.nome).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nome já registrado")

    #Pegar senha da requisição
    hashed_password = get_password_hash(user.senha)
    #Salvar informações do usuario no banco
    user_db = models.Users(nome=user.nome, senha=hashed_password, nivel=user.nivel)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    #Criar token de acesso e repassar ao usuario
    token = create_access_token(data={"sub": user.nome})
    return {"access_token": token, "token_type": "bearer"}

class RefreshTokenRequest(BaseModel):
    token: str

#Caso o token expire, o usuario pode acessar essa rota para voltar a logar
#Recebendo um token antigo e retornando um novo
@router.post("/refresh-token", response_model=Token)
def refresh_token(data: RefreshTokenRequest):
    #Validar o token antigo
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        nome = payload.get("sub")
        if not nome:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    #Criar novo e enviar ao usuario
    new_token = create_access_token(data={"sub": nome})
    return {"access_token": new_token, "token_type": "bearer"}