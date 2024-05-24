"""Хендлеры для сущности блюдо."""
from fastapi import APIRouter, Depends
from fastapi import HTTPException, Request
from starlette import status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from data_sources.models import get_async_session
from data_sources.storages.dish_repository import DishRepository
from pydantic_models.pydantic_model import DishModel

dish_router = APIRouter()


@dish_router.post('/api/v1/submenus/{target_submenu_id}/dishes')
async def create_dish(
    request: DishModel,
    target_submenu_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Создает новую позицию блюда."""

    return await DishRepository.create_dish(
        request.title,
        request.description,
        request.price,
        int(target_submenu_id),
        session,
    )


@dish_router.get('/api/v1/dishes/{target_dish_id}')
@cache(expire=30)
async def get_dish_item(
    request: Request,
    target_dish_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает объект блюдо определенной позиции блюда."""

    dish = await DishRepository.get_dish_by_id(int(target_dish_id), session)
    if dish:
        return dish
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'dish not found',
    )


@dish_router.patch('/api/v1/menus/submenus/{target_submenu_id}/dishes/{target_dish_id}')
async def update_dish(
    request: DishModel,
    target_submenu_id: int,
    target_dish_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновляет данные определенной позиции блюда."""

    return await DishRepository.update_dish(
        request.title,
        request.description,
        request.price,
        int(target_submenu_id),
        int(target_dish_id),
        session,
    )


@dish_router.delete('/api/v1/dishes/{target_dish_id}')
async def delete_dish(
    request: Request,
    target_dish_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаляет определенную позицию блюда."""

    return await DishRepository.delete_dish(int(target_dish_id), session)


@dish_router.get('/api/v1/dishes')
@cache(expire=3)
async def get_dishs_list(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех блюд."""

    return await DishRepository.get_dishs_list(session)
