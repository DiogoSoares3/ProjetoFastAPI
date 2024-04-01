from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.artigo_model import Artigo
from models.usuario_model import Usuario
from schemas.artigo_schema import ArtigoSchema
from core.deps import get_current_user, get_session


router = APIRouter()

# POST Artigo
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema,
                      usuario_logado: Usuario = Depends(get_current_user),
                      db: AsyncSession = Depends(get_session)
                      ) -> ArtigoSchema:
    print(usuario_logado)
    novo_artigo: Artigo = Artigo(titulo=artigo.titulo, descricao=artigo.descricao,
                                 url_fonte=str(artigo.url_fonte), usuario_id=usuario_logado.id)

    db.add(novo_artigo)
    await db.commit()
    await db.refresh(novo_artigo)
    
    return novo_artigo


# GET Artigos
@router.get('/', response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)) -> List[ArtigoSchema]:
    artigos : List[Artigo] = (await db.execute(select(Artigo))).scalars().unique().all()

    return artigos


# GET Artigo
@router.get('/{artigo_id}', response_model=ArtigoSchema)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    artigo: Artigo = (await db.execute(select(Artigo).filter(Artigo.id == artigo_id))).scalars().unique().one_or_none()
    
    if artigo:
        return artigo
    else:
        raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)


# PUT Artigo
@router.put('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def get_artigo(artigo_id: int, artigo: ArtigoSchema,
                     db: AsyncSession = Depends(get_session),
                     usuario_logado: Usuario = Depends(get_current_user)
                     ):
    artigo_up: Artigo = (await db.execute(select(Artigo).where(Artigo.id == artigo_id))).scalars().unique().one_or_none()

    if artigo_up:
        artigo_up.titulo = artigo.titulo
        artigo_up.descricao = artigo.descricao
        artigo_up.url_fonte = str(artigo.url_fonte)

        if usuario_logado.id != artigo_up.usuario_id: # Mudando o id de usuario do artigo se ele for atualizado
            artigo_up.usuario_id = usuario_logado.id

        await db.commit()

        return artigo_up
    else:
        raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)


# DELETE Artigo
@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session),
                     usuario_logado: Usuario = Depends(get_current_user)
                     ):
    artigo_del: Artigo = (await db.execute(select(Artigo).where(Artigo.id == artigo_id))).scalars().unique().one_or_none()

    if artigo_del:
        if usuario_logado.id != artigo_del.usuario_id: 
            raise HTTPException(detail='Só o autor do artigo pode deletar o artigo', status_code=status.HTTP_403_FORBIDDEN)

        await db.delete(artigo_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)
