from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.usuarios_model import Usuario
from core.configs import settings
from core.security import verificar_senha
from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)


async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[Usuario]:
    usuario: Usuario = (await db.execute(select(Usuario).where(Usuario.email == email))).scalars().unique().one_or_none() # Usando "unique()" pois as informações de usuarios também estão em outra tabela

    if not usuario:
        return None

    if not verificar_senha(senha, usuario.senha):
        return None

    return usuario


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}

    timezone_ = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=timezone_) + tempo_vida
    
    payload["type"] = tipo_token
    payload["exp"] = expire
    payload["iat"] = datetime.now(tz=timezone_)  # Gerado em...
    payload["sub"] = sub
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    """
    https://jwt.io
    """
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )