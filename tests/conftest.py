import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mader import _settings as Settings
from mader.app import app
from mader.database import get_session
from mader.models.Autores import Autores
from mader.models.base_model import Base
from mader.models.User import User
from mader.models.Livros import Livros
from mader.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


# @pytest.fixture(scope='session')
# def engine():
#     with PostgresContainer('postgres:17', driver='psycopg') as postgres:
#         Settings.TEST = True
#         yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session():
    Settings.TEST = True

    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest_asyncio.fixture
async def user(session):
    password = 'test'

    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'alice'

    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def livro(session, autor):
    db_livros = Livros(
        ano = 1937,
        titulo = 'Pense Enriqueça',
        id_autor = autor.id,
    )

    session.add(db_livros)
    await session.commit()
    await session.refresh(db_livros)

    return db_livros

@pytest_asyncio.fixture
async def autor(session):
    db_autores = Autores(name='Napoleon Hill')

    session.add(db_autores)
    await session.commit()
    await session.refresh(db_autores)

    return db_autores


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}44b73624c7')
