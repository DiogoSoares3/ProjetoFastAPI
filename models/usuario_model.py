from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings


class Usuario(settings.DBBaseModel):
    __tablename__ = 'usuarios'
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(256), nullable=True)
    sobrenome: str = Column(String(256), nullable=True)
    email: str = Column(String(256), nullable=False, unique=True)
    senha: str = Column(String(256), nullable=False)
    eh_admin = Column(Boolean, default=False)
    artigos = relationship(
        "Artigo", cascade="all,delete-orphan",  # Se deletar algum usuário, remove todos os seus artigos
        back_populates="criador", uselist=True, lazy="joined"
        )
