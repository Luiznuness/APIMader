from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from mader import _settings as Settings
from mader.models.base_model import Base

engine = create_async_engine(Settings.DATABASE_URL, echo=True)


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def create_table(engine):  # pragma: no cover
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def lifespan(app):  # pragma: no cover
    if Settings.TEST:
        yield
    else:
        await create_table(engine)
        yield
