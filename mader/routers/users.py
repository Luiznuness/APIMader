from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models.User import User
from mader.schemas import (
    CreatedUser,
    FilterPage,
    ListUser,
    Message,
    UserPublic,
)
from mader.security import get_current_user, get_password_hash

routers = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@routers.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def created_user(user: CreatedUser, session: T_Session):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@routers.get('/', status_code=HTTPStatus.OK, response_model=ListUser)
async def get_users(
    session: T_Session, filter_user: Annotated[FilterPage, Query()]
):
    db_users = await session.scalars(
        select(User).offset(filter_user.offset).limit(filter_user.limit)
    )

    return {'users': db_users}


@routers.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
async def get_user(user_id: int, session: T_Session):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return db_user


@routers.put(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
async def put_user(
    user: CreatedUser,
    user_id: int,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@routers.delete(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
async def deleted_user(
    user_id: int,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
