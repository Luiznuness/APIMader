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
from mader.models.Livros import Livros
from mader.models.User import User
from mader.schemas import (
    Books,
    BooksPublic,
    FilterBooks,
    ListBooks,
    UpdateBook,
)
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
    db_autor = await session.scalar(
        select(Autores).where(Autores.id == id_autor)
    )

    if not db_autor:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Autor not exists'
        )

    db_livro = Livros(
        ano=livro.ano,
        titulo=livro.titulo.strip().title(),
        id_autor=id_autor,
    )

    session.add(db_livro)
    await session.commit()
    await session.refresh(db_livro)

    return db_livro


@routers.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=ListBooks,
)
async def get_livros(
    current_user: CurrentUser,
    session: T_Session,
    filter_book: Annotated[FilterBooks, Query()],
):
    query = select(
        Livros.id,
        Livros.titulo,
        Livros.ano,
        Livros.id_autor,
        Autores.name.label('autor'),
    ).join(Autores, Livros.id_autor == Autores.id)

    if filter_book.titulo:
        query = query.filter(
            Livros.titulo.contains(
                filter_book.titulo.strip().title()
                )
            )

    if filter_book.ano:
        query = query.filter(Livros.ano.contains(filter_book.ano))

    books = await session.execute(
        query.limit(filter_book.limit).offset(filter_book.offset)
    )

    return {'books': books.mappings().all()}


@routers.patch(
    '/{id_autor}',
    status_code=HTTPStatus.OK,
    response_model=BooksPublic,
)
async def patch_books(
    session: T_Session,
    current_user: CurrentUser,
    id_autor: int,
    update_book: UpdateBook,
):
    db_autor = await session.scalar(
        select(Livros).where(Livros.id_autor == id_autor)
    )

    if not db_autor:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Autor not exists'
        )

    for chave, valor in update_book.model_dump(exclude_unset=True).items():
        if chave == 'titulo':
            valor = valor.strip().title()
        setattr(db_autor, chave, valor)

    session.add(db_autor)
    await session.commit()
    await session.refresh(db_autor)

    return db_autor
