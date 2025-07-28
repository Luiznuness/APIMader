from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models.User import User
from mader.schemas import Token
from mader.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

routers = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[AsyncSession, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[User, Depends(get_current_user)]


@routers.post(
    '/token',
    status_code=HTTPStatus.CREATED,
    response_model=Token,
)
async def created_token(
    session: T_Session,
    form_data: OAuth2Form,
):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    error = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Incorrect email ou password',
    )

    if not user:
        raise error

    if not verify_password(form_data.password, user.password):
        raise error

    data = {'sub': user.email}

    access_token = create_access_token(data)

    return {'access_token': access_token, 'token_type': 'Bearer'}


@routers.post(
    '/refresh-token',
    status_code=HTTPStatus.CREATED,
    response_model=Token,
)
async def refresh_token(current_user: CurrentUser):
    new_access_token = create_access_token(data={'sub': current_user.email})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}
