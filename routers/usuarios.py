from datetime import datetime, timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import models
from models.database import SessionLocal
from schemas.usuarios import UsuarioSchema, Token

router = APIRouter()

SECRET_KEY = "secreto-superseguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 padrão
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.nome == form_data.username).first()
    if not user or not verify_password(form_data.password, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token(data={"sub": user.nome})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=Token)
def register(user: UsuarioSchema, db: Session = Depends(get_db)):
    existing = db.query(models.Users).filter(models.Users.nome == user.nome).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nome já registrado")

    hashed_password = get_password_hash(user.senha)
    user_db = models.Users(nome=user.nome, senha=hashed_password, nivel=user.nivel)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    token = create_access_token(data={"sub": user.nome})
    return {"access_token": token, "token_type": "bearer"}

# class RefreshTokenRequest(BaseModel):
#     token: str

# @router.post("/refresh-token", response_model=Token)
# def refresh_token(data: RefreshTokenRequest):
#     try:
#         payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         if not email:
#             raise HTTPException(status_code=401, detail="Token inválido")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token inválido")
#
#     new_token = create_access_token(data={"sub": email})
#     return {"access_token": new_token, "token_type": "bearer"}