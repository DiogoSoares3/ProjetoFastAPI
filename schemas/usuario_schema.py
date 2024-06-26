from typing import Optional, List
from pydantic import BaseModel, EmailStr
from schemas.artigo_schema import ArtigoSchema

class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None 
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        from_attributes = True
        #orm_mode = True    # Deprecated


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str
    # Senha é só de acesso interno, ele não deve ser exposto, por isso devemos ter um schema separado


class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]
    # O retorno default de usuarios não precisa ter a lista de artigos
    # Só se especificar que quer os artigos de um usuario


class UsuarioSchemaUp(UsuarioSchemaBase): # Schema para update de usuários
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    eh_admin: Optional[bool] = None
