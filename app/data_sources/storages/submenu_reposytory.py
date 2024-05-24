"""Операции с данными для сущности подменю."""
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic_models.pydantic_model import SubmenuModelResp, SubmenuModelRespGetItem
from data_sources.models import Submenu_model, Dish_model
from data_sources.storages.menu_repository import MenuRepository


class SubMenuRepository:
    """Репозиторий для сущности подменю."""

    @classmethod
    async def get_submenu_by_name(cls, submenu_name: str, session: AsyncSession):
        """Возвращает объект подменю для определенной позиции подменю по имени."""

        query = select(Submenu_model).where(
            Submenu_model.c.title == submenu_name)
        exists_submenu = await session.execute(query)
        exists_submenu = exists_submenu.all()
        if len(exists_submenu) > 0:
            return exists_submenu
        return False

    @classmethod
    async def get_submenu_by_id(cls, submenu_id: int, session: AsyncSession):
        """Возвращает объект подменю для определенной позиции подменю по id."""

        query = select(Submenu_model).where(Submenu_model.c.id == submenu_id)
        exists_submenu = await session.execute(query)
        exists_submenu = exists_submenu.all()
        if len(exists_submenu) > 0:
            return exists_submenu
        return False

    @classmethod
    async def get_id_by_name(cls, submenu_name: str, session: AsyncSession):
        """Возвращает id определенного подменю по имени."""

        query = select(Submenu_model).where(
            Submenu_model.c.title == submenu_name)
        exists_submenu = await session.execute(query)
        exists_submenu = exists_submenu.all()
        if len(exists_submenu) != 0:
            return exists_submenu[0][0]
        return False

    @classmethod
    async def get_submenu_item(cls, submenu_id: int, session: AsyncSession):
        """Возвращает объект подменю с информацие о количестве блюд
        для данной позиции подменю.
        """

        exists_submenu = await cls.get_submenu_by_id(submenu_id, session)
        if not exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'submenu not found',
            )
        query = select(Dish_model).filter(
            Dish_model.c.from_submenu == submenu_id)
        dish_list = await session.execute(query)
        dish_list = dish_list.all()
        return SubmenuModelRespGetItem(
            id=exists_submenu[0][0],
            title=exists_submenu[0][1],
            description=exists_submenu[0][2],
            count_of_dishs=len(dish_list),
        )

    @classmethod
    async def create_submenu(
        cls,
        submenu_name: str,
        description: str,
        from_menu: int,
        session: AsyncSession,
    ):
        """Создает новую позицию подменю."""

        exists_submenu = await cls.get_submenu_by_name(submenu_name, session)
        if exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю {submenu_name} уже существует',
            )
        exists_menu = await MenuRepository.get_menu_by_id(from_menu, session)

        if not exists_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню с id {from_menu} не существует',
            )
        try:
            query = Submenu_model.insert().values(
                title=submenu_name,
                description=description,
                from_menu=from_menu,
            )
            await session.execute(query)
            await session.commit()
        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        try:
            submenu = await cls.get_submenu_by_name(submenu_name, session)
            return SubmenuModelResp(
                id=submenu[0][0],
                title=submenu[0][1],
                description=submenu[0][2],
            )
        except Exception:
            return {"detail": "Ошибка при отправке ответа"}

    @classmethod
    async def update_submenu(
        cls,
        title: str,
        description: str,
        from_menu: int,
        submenu_id: int,
        session: AsyncSession,
    ):
        """Обновляет данные для определенной позиции подменю."""

        exists_new_submenu_name = await cls.get_submenu_by_name(title, session)
        if exists_new_submenu_name:
            if exists_new_submenu_name[0][0] != submenu_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Подменю {title} уже существует',
                )
        exists_submenu = await cls.get_submenu_by_id(submenu_id, session)
        exists_menu = await MenuRepository.get_menu_by_id(from_menu, session)
        if not exists_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню с id {from_menu} не существует',
            )
        if not exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'submenu not found',
            )
        try:
            query = Submenu_model.update().where(
                Submenu_model.c.id == submenu_id,
            ).values(
                title=title,
                description=description,
                from_menu=from_menu
            )
            await session.execute(query)
            await session.commit()
        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        try:
            submenu = await cls.get_submenu_by_name(title, session)
            return SubmenuModelResp(
                id=submenu[0][0],
                title=submenu[0][1],
                description=submenu[0][2],
            )
        except Exception:
            return {"detail": "Ошибка при отправке ответа"}

    @classmethod
    async def delete_submenu(cls, target_submenu_id: int, session: AsyncSession):
        """Удаляет определенную позицию подменю.
        Так же удаляет все связанные позиции блюд.
        """

        exists_submenu = await cls.get_submenu_by_id(target_submenu_id, session)
        if not exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'submenu not found',
            )
        try:
            query = Dish_model.delete().where(Dish_model.c.from_submenu == target_submenu_id)
            await session.execute(query)
            query2 = Submenu_model.delete().where(Submenu_model.c.id == target_submenu_id)
            await session.execute(query2)
            await session.commit()
            return {"status": True,
                    "message": "The submenu has been deleted",
                    }

        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}

    @classmethod
    async def get_submenu_list(cls, session: AsyncSession):
        """Возвращает словарь со списком всех позиций подменю.
        Для каждой позиции подменю указано количество соответствующих
        данной позиции подменю позиций блюд.
        """

        query = select(Submenu_model)
        submenu_list = await session.execute(query)
        submenu_list = submenu_list.all()
        if len(submenu_list) == 0:
            return {}
        response = {}

        for submenu in submenu_list:
            query = select(Dish_model).filter(
                Dish_model.c.from_submenu == submenu[0])
            dish_list = await session.execute(query)
            dish_list = dish_list.all()
            response[submenu[1]] = {
                "id": submenu[0],
                "title": submenu[1],
                "description": submenu[2],
                "count_of_dishs": len(dish_list),
            }
        return response
