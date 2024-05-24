"""Файл запуска приложения."""
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import uvicorn
from views.crud_for_menu import menu_router
from views.crud_for_submenu import submenu_router
from views.crud_for_dish import dish_router
from config import settings


def get_application() -> FastAPI:
    """Возвращает экземпляр приложения.

    Returns:
        FastAPI: _description_
    """
    application = FastAPI()
    return application


application = get_application()
application.include_router(menu_router)
application.include_router(submenu_router)
application.include_router(dish_router)


@application.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        f"redis://{settings.redis_host}:{settings.redis_port}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

if __name__ == '__main__':
    uvicorn.run(
        app=application,
        host=settings.app_host,
        port=int(settings.app_port),
    )
