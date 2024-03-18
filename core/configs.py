from typing import List, ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
    '''
    Configurações gerais usadas na aplicação
    '''

    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/faculdade'
    DBBaseModel: ClassVar = declarative_base()
    
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    
    JWT_SECRET: str = secret_key  # Quando trabalhamos com tokens, o padrão é o JSON Web Token (JWT)
    
    '''
    import secrets
    
    token: str = secrets.token_urlsafe(32)
    '''
    
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # Ou seja, o token está valido por uma semana

    class Config:
        case_sensitive = True


settings: Settings = Settings()
