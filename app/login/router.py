from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..security import verify_password, create_access_token, get_current_user
from .repository import UsuarioRepository
from .. import model
from . import schema

router = APIRouter(prefix="/login", tags=["Login"])

# --- ENDPOINT DE LOGIN ---
@router.post("/", response_model=schema.TokenResponse)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    repo = UsuarioRepository()
    # Usa o repositório local para encontrar o usuário
    user = repo.find_by_email(db, email=form_data.username)
    
    # Verifica a senha e o status
    if not user or not user.status == model.StatusContaEnum.ATIVO or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos, ou usuário não ativo.",
        )
    
    # Cria o token se as credenciais estiverem corretas
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ENDPOINT DE VERIFICAÇÃO DE TOKEN ---
@router.get("/me", response_model=schema.UsuarioResponse)
def read_users_me(current_user: model.Usuario = Depends(get_current_user)):
    """
    Este endpoint é usado por outros serviços para validar um token.
    Se o token enviado no cabeçalho for válido, ele retorna os dados do usuário.
    Se for inválido, a função 'get_current_user' irá retornar um erro 401.
    """
    return current_user