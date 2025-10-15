from pydantic import BaseModel, EmailStr
from ..model import StatusContaEnum

# Schema para a resposta do token de login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Schema para a resposta dos dados de um usuário
class UsuarioResponse(BaseModel):
    id: int
    cpf: str
    nome: str
    email: EmailStr
    status: StatusContaEnum
    tipo_usuario: str

    class Config:
        from_attributes = True # Equivalente ao orm_mode = True