from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..security import verify_password, create_access_token, get_current_user
from .repository import UsuarioRepository
from .. import model
from . import schema

router = APIRouter(prefix="/login", tags=["Login"])
@router.post("/", response_model=schema.TokenResponse)
def login_for_access_token(db: Session = Depends(get_db), username: str = Form(), password: str = Form()):
    repo = UsuarioRepository()
    user = repo.find_by_email(db, email=username)
    
    if not user or not user.status == model.StatusContaEnum.ATIVO or not verify_password(password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos, ou usuário não ativo.",
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schema.UsuarioResponse)
def read_users_me(current_user: model.Usuario = Depends(get_current_user)):
    return current_user