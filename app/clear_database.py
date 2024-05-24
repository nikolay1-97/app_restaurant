import asyncio

from data_sources.models import (
    Menu_model,
    Submenu_model,
    Dish_model,
    async_session_maker,
)


async def clear_tables():
    """Удаляет все данные из всех таблиц базы данных."""

    async with async_session_maker() as session:
        try:
            stmt1 = Dish_model.delete()
            stmt2 = Submenu_model.delete()
            stmt3 = Menu_model.delete()
            await session.execute(stmt1)
            await session.execute(stmt2)
            await session.execute(stmt3)
            await session.commit()
        except Exception as some_ex:
            print(some_ex)
            await session.rollback()

asyncio.run(clear_tables())
