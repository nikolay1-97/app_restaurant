from sqlalchemy import insert
from data_sources.models import Menu_model, Submenu_model, Dish_model
from src.tests.conftest import async_session_maker
import asyncio

async def create_menu():
    async with async_session_maker() as session:
        stmt = insert(Menu_model).values(
            id=5,
            title='menu2',
            description='my menu2',
        )
        await session.execute(stmt)
        await session.commit()

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

asyncio.run(create_menu(), create_submenu(), create_dish())