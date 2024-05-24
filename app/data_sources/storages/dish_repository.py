"""Операции с данными для сущности блюдо."""
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_sources.models import Dish_model
from data_sources.storages.submenu_reposytory import SubMenuRepository


class DishRepository:
    """Репозиторий для сущности блюдо."""

    @classmethod
    async def get_dish_by_name(cls, dish_name: str, session: AsyncSession):
        """Возвращает словарь с данными для
        определенной позиции блюда по имени блюда.
        """

        query = select(Dish_model).where(Dish_model.c.title == dish_name)
        exists_dish = await session.execute(query)
        exists_dish = exists_dish.all()
        if len(exists_dish) > 0:
            return {
                "id": exists_dish[0][0],
                "title": exists_dish[0][1],
                "description": exists_dish[0][2],
                "price": round(exists_dish[0][3], 2),
            }
        return False

    @classmethod
    async def get_id_by_name(cls, dish_name: str, session: AsyncSession):
        """Возвращает id по имени блюда."""

        query = select(Dish_model).where(Dish_model.c.title == dish_name)
        exists_dish = await session.execute(query)
        exists_dish = exists_dish.all()
        if len(exists_dish) != 0:
            return exists_dish[0][0]
        return False

    @classmethod
    async def get_dish_by_id(cls, dish_id: int, session: AsyncSession):
        """Возвращает словарь с данными для
        определенной позиции блюда по id блюда.
        """

        query = select(Dish_model).where(Dish_model.c.id == dish_id)
        exists_dish = await session.execute(query)
        exists_dish = exists_dish.all()
        if len(exists_dish) > 0:
            return {
                "id": exists_dish[0][0],
                "title": exists_dish[0][1],
                "description": exists_dish[0][2],
                "price": round(exists_dish[0][3], 2),
            }
        return False

    @classmethod
    async def create_dish(
        cls,
        dish_name: str,
        description: str,
        price: str,
        from_submenu: int,
        session: AsyncSession,
    ):
        """Создает новую позицию блюда."""

        try:
            price = float(price)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'аргумент price должен быть вещественным числом'
            )
        exists_dish = await cls.get_dish_by_name(dish_name, session)
        if exists_dish:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Наименование блюда {dish_name} уже существует',
            )
        exists_submenu = await SubMenuRepository.get_submenu_by_id(from_submenu, session)
        if not exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю с id {from_submenu} не существует',
            )
        try:
            query = Dish_model.insert().values(
                title=dish_name,
                description=description,
                price=float(price),
                from_submenu=int(from_submenu),
            )
            await session.execute(query)
            await session.commit()
        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        try:
            return await cls.get_dish_by_name(dish_name, session)
        except Exception:
            {"detail": "Ошибка при отправке ответа"}

    @classmethod
    async def update_dish(
        cls,
        dish_name: str,
        description: str,
        price: str,
        from_submenu: int,
        dish_id: int,
        session: AsyncSession,
    ):
        """Обновляет данные определенной позиции блюда."""

        try:
            price = float(price)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'аргумент цена должен быть вещественным числом'
            )
        exists_new_dish_name = await cls.get_dish_by_name(dish_name, session)
        if exists_new_dish_name:
            if exists_new_dish_name['id'] != dish_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Наименование блюда {dish_name} уже существует',
                )
        exists_dish = await cls.get_dish_by_id(dish_id, session)
        exists_submenu = await SubMenuRepository.get_submenu_by_id(from_submenu, session)
        if not exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю с id {from_submenu} не существует',
            )

        if not exists_dish:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'dish not found',
            )
        try:
            query = Dish_model.update().where(
                Dish_model.c.id == dish_id,
            ).values(
                title=dish_name,
                description=description,
                price=float(price),
                from_submenu=int(from_submenu),
            )
            await session.execute(query)
            await session.commit()
        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        try:
            return await cls.get_dish_by_name(dish_name, session)
        except Exception:
            {"detail": "Ошибка при отправке ответа"}

    @classmethod
    async def delete_dish(cls, target_dish_id: int, session: AsyncSession):
        """Удаляет определенную позицию блюда."""

        exists_dish = await cls.get_dish_by_id(target_dish_id, session)
        if not exists_dish:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'dish not found',
            )
        try:
            query = Dish_model.delete().where(Dish_model.c.id == target_dish_id)
            await session.execute(query)
            await session.commit()
            return {
                "status": True,
                "message": "The dish has been deleted"
            }
        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}

    @classmethod
    async def get_dishs_list(cls, session: AsyncSession):
        """Возвращает словарь со списком всех позиций блюд."""

        query = select(Dish_model)
        dish_list = await session.execute(query)
        dish_list = dish_list.all()
        if len(dish_list) == 0:
            return {}
        response = {}

        for i in range(len(dish_list)):
            response[dish_list[i][1]] = {
                "id": dish_list[i][0],
                "title": dish_list[i][1],
                "description": dish_list[i][2],
                "price": round(dish_list[i][3], 2),
            }
        return response
