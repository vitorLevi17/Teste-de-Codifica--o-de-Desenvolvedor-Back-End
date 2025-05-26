from pydantic import BaseModel
"""
    Schemas relacionados para autenticação do usuario
"""
#Schema para receber dados de criação do usuario
class UsuarioSchema(BaseModel):
    nome : str
    senha : str
    nivel : str

#Schema para receber token
class Token(BaseModel):
    access_token: str
    token_type: str