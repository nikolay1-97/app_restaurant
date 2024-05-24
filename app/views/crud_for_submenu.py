"""Хендлеры для сущности подменю."""
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from data_sources.models import get_async_session
from data_sources.storages.submenu_reposytory import SubMenuRepository
from pydantic_models.pydantic_model import SubmenuModel

submenu_router = APIRouter()


@submenu_router.post('/api/v1/menus/{target_menu_id}/submenus')
async def create_submenu(
    request: SubmenuModel,
    target_menu_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Создает новую позицию подменю."""

    return await SubMenuRepository.create_submenu(
        request.title,
        request.description,
        int(target_menu_id),
        session,
    )


@submenu_router.get('/api/v1/submenus/{target_submenu_id}')
@cache(expire=30)
async def get_submenu_item(
    request: Request,
    target_submenu_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает объект подменю для определенной позиции подменю."""

    return await SubMenuRepository.get_submenu_item(int(target_submenu_id), session)


@submenu_router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def update_submenu(
    request: SubmenuModel,
    target_menu_id: int,
    target_submenu_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновляет данные для определенной позиции подменю."""

    return await SubMenuRepository.update_submenu(
        request.title,
        request.description,
        int(target_menu_id),
        int(target_submenu_id),
        session,
    )


@submenu_router.delete('/api/v1/submenus/{target_submenu_id}')
async def delete_submenu(
    request: Request,
    target_submenu_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаляет определенную позицию подменю."""

    return await SubMenuRepository.delete_submenu(int(target_submenu_id), session)


@submenu_router.get('/api/v1/submenus')
@cache(expire=3)
async def get_submenu_list(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех позиций подменю."""

    return await SubMenuRepository.get_submenu_list(session)
