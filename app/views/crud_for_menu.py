"""Хендлеры для сущности меню."""
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from data_sources.models import get_async_session
from pydantic_models.pydantic_model import MenuModel
from data_sources.storages.menu_repository import MenuRepository

menu_router = APIRouter()


@menu_router.post('/api/v1/menus')
async def create_menu(
    request: MenuModel,
    session: AsyncSession = Depends(get_async_session),
):
    """Создает новую позицию меню."""

    return await MenuRepository.create_menu(
        request.title,
        request.description,
        session,
    )


@menu_router.patch('/api/v1/menus/{target_menu_id}')
async def update_menu(
    request: MenuModel,
    target_menu_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновляет данные определенной позиции меню."""

    return await MenuRepository.update_menu(
        request.title,
        request.description,
        int(target_menu_id),
        session,
    )


@menu_router.get('/api/v1/menus/{target_menu_id}')
@cache(expire=30)
async def get_menu_item(
    request: Request,
    target_menu_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает объект меню для определенной позиции меню."""

    return await MenuRepository.get_menu_item(int(target_menu_id), session)


@menu_router.delete('/api/v1/menus/{target_menu_id}')
async def delete_menu(
    request: Request,
    target_menu_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаляет определенную позицию меню."""

    return await MenuRepository.delete_menu(int(target_menu_id), session)


@menu_router.get('/api/v1/menus')
@cache(expire=3)
async def get_menu_list(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех позиций меню."""

    return await MenuRepository.get_menu_list(session)
