"""Конфигурация для тестов."""
import pytest
import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import insert

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.data_sources.models import get_async_session
from app.data_sources.models import metadata
from app.config import TEST_DB_URL
from app.main import application
from app.data_sources.models import Menu_model, Submenu_model, Dish_model

engine_test = create_async_engine(TEST_DB_URL, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

application.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)

# SETUP


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(application)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=application),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(autouse=True, scope='session')
async def func():
    redis = aioredis.from_url(
        "redis://localhost",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@pytest.fixture(scope="function")
async def create_menu():
    async with async_session_maker() as session:
        stmt = insert(Menu_model).values(
            id=5,
            title='menu2',
            description='my menu2',
        )
        await session.execute(stmt)
        await session.commit()


@pytest.fixture(scope="function")
async def create_submenu():
    async with async_session_maker() as session:
        stmt = insert(Menu_model).values(
            id=7,
            title='menu3',
            description='my menu3',
        )
        await session.execute(stmt)
        await session.commit()

    async with async_session_maker() as session:
        stmt = insert(Submenu_model).values(
            id=3,
            title='submenu2',
            description='my submenu2',
            from_menu=7,
        )
        await session.execute(stmt)
        await session.commit()


@pytest.fixture(scope="function")
async def create_dish():
    async with async_session_maker() as session:
        stmt = insert(Dish_model).values(
            id=7,
            title='dish5',
            description='my dish5',
            price=250.00,
            from_submenu=3,
        )
        await session.execute(stmt)
        await session.commit()
