import pytest
from sqlalchemy import select

from mader.models.User import User


@pytest.mark.asyncio
async def test_add_db(session):
    dados_db = User(
        username='Luiz', email='luiz@test.com', password='LuizTeste'
    )

    session.add(dados_db)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.username == dados_db.username)
    )

    assert user.as_dict()
