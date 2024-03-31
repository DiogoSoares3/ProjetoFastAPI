from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.future import select
from pydantic import BaseModel
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import Usuario


class TokenData(BaseModel):
    username: Optional[str] = None


async def get_session() -> AsyncGenerator:
    session: AsyncSession = Session()
    try:
        yield session  # Fica preso no try até finalizar
    finally:
        await session.close()


async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)) -> Usuario:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credenticial",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:  # Decodificando o token
        payload = jwt.decode(
            token,
            key=settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        username: str = payload.get("sub") # Obtendo o ID do usuário desse token decodificado

        if username is None:
            raise credential_exception

        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credential_exception

    # Buscando informações do usuário que tem esse token
    usuario: Usuario = (await db.execute(select(Usuario).where(Usuario.id == int(token_data.username)))).scalars().unique().one_or_none()

    if usuario is None:
        raise credential_exception

    return usuario
