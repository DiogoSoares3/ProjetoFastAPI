from typing import Optional
from pydantic import BaseModel, HttpUrl

class ArtigoSchema(BaseModel):
    id: Optional[int] = None 
    titulo: str
    url_fonte: HttpUrl
    descricao: str
    usuario_id: Optional[int] = None

    class Config:
        from_attributes = True
        #orm_mode = True    # Deprecated
