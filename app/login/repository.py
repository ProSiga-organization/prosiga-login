from sqlalchemy.orm import Session
from .. import model

class UsuarioRepository:
    @staticmethod
    def find_by_email(db: Session, email: str) -> model.Usuario | None:
        return db.query(model.Usuario).filter(model.Usuario.email == email).first()