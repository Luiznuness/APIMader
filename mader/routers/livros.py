from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models.Autores import Autores
from mader.models.Livros import Livros
from mader.models.User import User
from mader.schemas import Books, BooksPublic
from mader.security import get_current_user

T_Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

routers = APIRouter(prefix='/livros', tags=['livros'])


@routers.post(
    '/{id_autor}', status_code=HTTPStatus.CREATED, response_model=BooksPublic
)
async def created_book(
    session: T_Session,
    current_user: CurrentUser,
    id_autor: int,
    livro: Books,
):
    livro.titulo = livro.titulo.strip().title()

    db_autor = await session.scalar(
        select(Autores).where(Autores.id == id_autor)
    )

    if not db_autor:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Autor not exists'
        )

    db_livro = Livros(
        ano=livro.ano,
        titulo=livro.titulo,
        id_autor=id_autor,
    )

    session.add(db_livro)
    await session.commit()
    await session.refresh(db_livro)

    return db_livro
