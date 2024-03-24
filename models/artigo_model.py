from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class Artigo(settings.DBBaseModel):
    __tablename__ = 'artigos'
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    titulo: str = Column(String(256))
    url_fonte: str = Column(String(256))
    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'))
    criador: relationship(
        "Usuario", back_populates='artigos', lazy='joined'
        ) # type: ignore
