from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    nome : str
    senha : str
    nivel : str

class Token(BaseModel):
    access_token: str
    token_type: str