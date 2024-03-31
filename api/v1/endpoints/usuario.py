from typing import List, Optional, AnyStr
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models.usuario_model import Usuario
from schemas.usuario_schema import *
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()


# GET Logado
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: Usuario = Depends(get_current_user)):
    return usuario_logado


# POST / Sign up
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase) # Retornar sem a senha
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)): # Parametro 'usuario' com a senha
    novo_usuario: Usuario = Usuario(nome=usuario.nome, sobrenome=usuario.sobrenome, 
                                    email=usuario.email, senha=gerar_hash_senha(usuario.senha),
                                    eh_admin=usuario.eh_admin)
    
    try:
        db.add(novo_usuario)
        await db.commit()
        
        return novo_usuario
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Esse email já é utilizado na plataforma")
        


# GET usuarios
@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    usuarios: List[Usuario] = (await db.execute(select(Usuario))).scalars().unique().all() # Talvez precise de unique()
    
    return usuarios


# GET usuario
@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    usuario: Usuario = (await db.execute(select(Usuario).where(Usuario.id == usuario_id))).scalars().unique().one_or_none()
    
    if usuario:
        return usuario
    else:
        return HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


# PUT usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def get_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    usuario_up: Usuario = (await db.execute(select(Usuario).where(Usuario.id == usuario_id))).scalars().unique().one_or_none()
    
    if usuario_up: # Nesse codigo, por escolha, podemos atualizar o todos os atributos
        if usuario.nome:
            usuario_up.nome = usuario.nome
        if usuario.sobrenome:
            usuario_up.sobrenome = usuario.sobrenome
        if usuario.email:
            usuario_up.email = usuario.email
        if usuario.senha:
            usuario_up.senha = usuario.senha
        if usuario.eh_admin:
            usuario_up.eh_admin = usuario.eh_admin

        await db.commit()
        return usuario_up
    else:
        return HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


# DELETE usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    usuario_del: Usuario = (await db.execute(select(Usuario).where(Usuario.id == usuario_id))).scalars().unique().one_or_none()

    if usuario_del:
        await db.delete(usuario_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


# POST Login
@router.post('/login', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha incorreto")
    
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id),
                                 "token_type": "bearer"
                                 }, status_code=status.HTTP_200_OK)
    