from typing import Optional
from pydantic import BaseModel, HttpUrl
#from models.usuario_model import Usuario

class ArtigoSchema(BaseModel):
    id: Optional[int] = None 
    titulo: str
    url_fonte: HttpUrl
    descricao: str
    usuario_id: int
    #criador: Usuario

    class Config:
        from_attributes = True
        #orm_mode = True    # Deprecated
