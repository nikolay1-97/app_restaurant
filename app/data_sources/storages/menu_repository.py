"""Операции с данными для сущности меню."""
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic_models.pydantic_model import MenuModelResp, MenuModelRespGetItem
from data_sources.models import Menu_model, Submenu_model, Dish_model


class MenuRepository:
    """Репозиторий для сущности меню."""

    @classmethod
    async def get_menu_by_name(cls, menu_name: str, session: AsyncSession):
        """Возвращает объект меню для определенной позиции меню по имени."""

        query = select(Menu_model).where(Menu_model.c.title == menu_name)
        exists_menu = await session.execute(query)
        exists_menu = exists_menu.all()
        if len(exists_menu) > 0:
            return exists_menu
        return False

    @classmethod
    async def get_id_by_name(cls, menu_name: str, session: AsyncSession):
        """Возвращает id определенной позиции меню по имени."""

        query = select(Menu_model).where(Menu_model.c.title == menu_name)
        exists_menu = await session.execute(query)
        exists_menu = exists_menu.all()
        if len(exists_menu) != 0:
            return exists_menu[0][0]
        return False

    @classmethod
    async def get_menu_by_id(cls, menu_id: int, session: AsyncSession):
        """Возвращает объект меню для определенной позиции меню по id."""

        query = select(Menu_model).where(Menu_model.c.id == menu_id)
        exists_menu = await session.execute(query)
        exists_menu = exists_menu.all()
        if len(exists_menu) > 0:
            return exists_menu
        return False

    @classmethod
    async def get_menu_item(cls, menu_id: int, session: AsyncSession):
        """Возвращает объект меню с информацией о количестве подменю
        и блюд для данной позиции меню.
        """

        menu = await cls.get_menu_by_id(int(menu_id), session)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'menu not found'
            )
        query = select(Submenu_model).filter(
            Submenu_model.c.from_menu == int(menu_id))
        submenu_list = await session.execute(query)
        submenu_list = submenu_list.all()
        count_of_dishs = 0
        for submenu in submenu_list:
            query = select(Dish_model).filter(
                Dish_model.c.from_submenu == submenu.id)
            dish_list = await session.execute(query)
            dish_list = dish_list.all()
            count_of_dishs += len(dish_list)

        return MenuModelRespGetItem(
            id=menu[0][0],
            title=menu[0][1],
            description=menu[0][2],
            count_of_submenu=len(submenu_list),
            count_of_dishs=count_of_dishs,
        )

    @classmethod
    async def create_menu(cls, title: str, description: str, session: AsyncSession):
        """Создает новую позицию меню."""

        exists_menu = await cls.get_menu_by_name(title, session)
        if exists_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню {title} уже существует',
            )
        try:
            query = Menu_model.insert().values(title=title, description=description)
            await session.execute(query)
            await session.commit()
        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        try:
            menu = await cls.get_menu_by_name(title, session)
            return MenuModelResp(
                id=menu[0][0],
                title=menu[0][1],
                description=menu[0][2],
            )
        except Exception:
            return {"detail": "Ошибка при отправке ответа"}

    @classmethod
    async def update_menu(
        cls,
        title: str,
        description: str,
        menu_id: int,
        session: AsyncSession,
    ):
        """Обновляет данные для определенной позиции меню."""

        exists_new_menu_name = await cls.get_menu_by_name(title, session)
        if exists_new_menu_name:
            if exists_new_menu_name[0][0] != menu_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Меню {title} уже существует',
                )
        exists_menu = await cls.get_menu_by_id(menu_id, session)

        if exists_menu:
            try:
                query = Menu_model.update().where(
                    Menu_model.c.id == menu_id,
                ).values(
                    title=title,
                    description=description,
                )
                await session.execute(query)
                await session.commit()

            except Exception:
                await session.rollback()
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="menu not found",
            )
        try:
            menu = await cls.get_menu_by_id(menu_id, session)
            return MenuModelResp(
                id=menu[0][0],
                title=menu[0][1],
                description=menu[0][2],
            )
        except Exception:
            return {"detail": "Ошибка при отправке ответа"}

    @classmethod
    async def delete_menu(cls, target_menu_id: int, session: AsyncSession):
        """Удаляет определенную позицию меню.
        Так же удаляет все связанные позиции подменю и блюд.
        """

        exists_menu = await cls.get_menu_by_id(target_menu_id, session)
        if not exists_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'menu not found',
            )
        try:
            query = select(Submenu_model).filter(
                Submenu_model.c.from_menu == target_menu_id,
            )
            submenu_list = await session.execute(query)
            submenu_list = submenu_list.all()
            for submenu in submenu_list:
                query = Dish_model.delete().where(
                    Dish_model.c.from_submenu == submenu[0])
                await session.execute(query)

            query = Submenu_model.delete().where(Submenu_model.c.from_menu == target_menu_id)
            await session.execute(query)
            query2 = Menu_model.delete().where(Menu_model.c.id == target_menu_id)
            await session.execute(query2)
            await session.commit()
            return {"status": True,
                    "message": "The menu has been deleted"
                    }

        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}

    @classmethod
    async def get_menu_list(cls, session: AsyncSession):
        """Возвращает словарь с списком всех позиций меню.
        Для каждой позиции меню указано количество соответствующих
        данной позиции меню позиций подменю.
        """

        query = select(Menu_model)
        menu_list = await session.execute(query)
        menu_list = menu_list.all()
        if len(menu_list) == 0:
            return {}
        response = {}

        for menu in menu_list:
            count_of_dishs = 0
            query = select(Submenu_model).filter(
                Submenu_model.c.from_menu == menu[0])
            submenu_list = await session.execute(query)
            submenu_list = submenu_list.all()
            response[menu[1]] = {
                "id": menu[0],
                "title": menu[1],
                "description": menu[2],
                "count_of_submenu": len(submenu_list),
            }

            for submenu in submenu_list:
                query = select(Dish_model).filter(
                    Dish_model.c.from_submenu == submenu[0])
                dish_list = await session.execute(query)
                dish_list = dish_list.all()
                count_of_dishs += len(dish_list)

            response[menu[1]]['count_of_dishs'] = count_of_dishs
        return response
