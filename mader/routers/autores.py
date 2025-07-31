from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models.Autores import Autores
from mader.models.User import User
from mader.schemas import (
    Autor,
    AutorPublic,
    FilterAutor,
    ListAutorPublic,
    Message,
)
from mader.security import get_current_user

T_Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

routers = APIRouter(prefix='/autores', tags=['autores'])


@routers.post('/', status_code=HTTPStatus.CREATED, response_model=AutorPublic)
async def created_autor(
    session: T_Session,
    current_user: CurrentUser,
    autor: Autor,
):
    autor.name = autor.name.strip().title()

    db_autor = await session.scalar(
        select(Autores).where(Autores.name == autor.name)
    )

    if db_autor:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Autor already exists'
        )

    db_autor = Autores(name=autor.name)

    session.add(db_autor)
    await session.commit()
    await session.refresh(db_autor)

    return db_autor


@routers.get('/', status_code=HTTPStatus.OK, response_model=ListAutorPublic)
async def get_autores(
    session: T_Session,
    current_user: CurrentUser,
    filter_autor: Annotated[FilterAutor, Query()],
):
    db_autor = select(Autores)

    if filter_autor.name:
        db_autor = db_autor.filter(
            Autores.name.contains(filter_autor.name.title())
        )

    autores = await session.scalars(
        db_autor.offset(filter_autor.offset).limit(filter_autor.limit)
    )

    return {'autores': autores.all()}


@routers.get(
    '/{id_autor}',
    status_code=HTTPStatus.OK,
    response_model=AutorPublic,
)
async def get_autor_id(
    id_autor: int,
    session: T_Session,
    current_user: CurrentUser,
):
    db_autor = await session.scalar(
        select(Autores).where(Autores.id == id_autor)
    )

    if not db_autor:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Autor not found'
        )

    return db_autor


@routers.put(
    '/{id_autor}',
    status_code=HTTPStatus.OK,
    response_model=AutorPublic,
)
async def put_autor(
    session: T_Session,
    current_user: CurrentUser,
    id_autor: int,
    autor: Autor,
):
    db_autor = await session.scalar(
        select(Autores).where(Autores.id == id_autor)
    )

    if not db_autor:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Autor not found'
        )

    db_autor.name = autor.name

    session.add(db_autor)
    await session.commit()
    await session.refresh(db_autor)

    return db_autor


@routers.delete(
    '/{id_autor}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
async def delete_autor(
    id_autor: int,
    session: T_Session,
    current_user: CurrentUser,
):
    db_autor = await session.scalar(
        select(Autores).where(Autores.id == id_autor)
    )

    if not db_autor:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Autor not found',
        )

    await session.delete(db_autor)
    await session.commit()

    return {'message': 'Autor deleted'}
