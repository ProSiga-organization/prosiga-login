from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..security import verify_password, create_access_token, get_current_user
from .repository import UsuarioRepository
from .. import model

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = UsuarioRepository.find_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user: model.Usuario = Depends(get_current_user)):
    # Este endpoint é para outros serviços verificarem um token.
    # Se o token for válido, ele retorna os dados do usuário.
    return current_user