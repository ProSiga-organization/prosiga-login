
from sqlalchemy import (
    Column, Integer, String, Boolean, Enum, Date, Float, ForeignKey
)
from sqlalchemy.orm import relationship
from .database import Base
import enum

class StatusContaEnum(str, enum.Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    NOVO = "NOVO"

class StatusAprovacaoEnum(str, enum.Enum):
    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"
    TRANCADO = "TRANCADO"
    EM_CURSO = "EM_CURSO"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: int = Column(Integer, primary_key=True, index=True)
    cpf: str = Column(String(11), unique=True, nullable=False, index=True)
    nome: str = Column(String(100), nullable=False)
    email: str = Column(String(100), unique=True, nullable=True, index=True)
    senha_hash: str = Column(String(255), nullable=False)
    status: StatusContaEnum = Column(Enum(StatusContaEnum), default=StatusContaEnum.NOVO)
    tipo_usuario: str = Column(String(50))

    __mapper_args__ = {
        "polymorphic_on": tipo_usuario,
        "polymorphic_identity": "usuario",
    }

class Aluno(Usuario):
    __mapper_args__ = {"polymorphic_identity": "aluno"}
    matricula: str = Column(String(20), unique=True)
    matriculas = relationship("Matricula", back_populates="aluno")

class Professor(Usuario):
    __mapper_args__ = {"polymorphic_identity": "professor"}
    turmas = relationship("Turma", back_populates="professor")

class Coordenador(Usuario):
    __mapper_args__ = {"polymorphic_identity": "coordenador"}

