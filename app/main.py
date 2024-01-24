"""Файл запуска приложения"""

from fastapi import FastAPI
from fastapi import HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from starlette import status
import uvicorn
from pydantic_models.pydantic_model import MenuModel
from data_sources.storages.menu_repository import (
    MenuRepository, SubMenuRepository, DishRepository,
)

from pydantic_models.pydantic_model import (MenuModel,
MenuModelUpdate, SubmenuModel, SubmenuModelUpdate, DishModel, DishModelUpdate
)

def get_application() -> FastAPI:
    """Возвращает экземпляр приложения.

    Returns:
        FastAPI: _description_
    """
    application = FastAPI()
    
    return application


application = get_application()


@application.post('/api/v1/menus')
def create_menu(request: MenuModel):
    return MenuRepository.create_menu(request.title, request.description)


@application.patch('/api/v1/menus/{target_menu_id}')
def update_menu(request: MenuModel, target_menu_id: str):
    return MenuRepository.update_menu(
        request.title,
        request.description,
        target_menu_id,
    )


@application.get('/api/v1/menus/{target_menu_id}')
def get_menu_by_name(request: Request, target_menu_id: str):
    menu = MenuRepository.get_menu_by_id(target_menu_id)
    if menu:
        return {'id': menu[0],
                'title': menu[1],
                'description': menu[2],
        }
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='menu not found',
        )
    
@application.delete('/api/v1/menus/{target_menu_id}')
def delete_menu(request: Request, target_menu_id: int):
    return MenuRepository.delete_menu(target_menu_id)


@application.get('/api/v1/menus')
def get_menu_list(request: Request):
    response = MenuRepository.get_menu_list()
    return response

# Операции с подменю.

@application.post('/api/v1/menus/{target_menu_id}/submenus')
def create_submenu(request: SubmenuModel, target_menu_id: int):
    return SubMenuRepository.create_submenu(
        request.title,
        request.description,
        target_menu_id,
    )

@application.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def get_submenu_item(
    request: Request,
    target_menu_id: int,
    target_submenu_id: int,
):
    submenu = SubMenuRepository.get_submenu_by_id(
        target_submenu_id,
    )
    
    if submenu:
        return {'id': submenu[0],
                'title': submenu[1],
                'description': submenu[2],
        }
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='submenu not found',
        )
    

@application.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def update_submenu(request: SubmenuModel, target_menu_id, target_submenu_id):
    return SubMenuRepository.update_submenu(
        request.title,
        request.description,
        target_menu_id,
        target_submenu_id,
    )


@application.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def delete_submenu(
    request: Request,
    target_menu_id: int,
    target_submenu_id: int,):
    return SubMenuRepository.delete_submenu(target_submenu_id)


@application.get('/api/v1/menus/{target_menu_id}/submenus')
def get_submenu_list(request: Request, target_menu_id: int):
    return SubMenuRepository.get_submenu_list(target_menu_id)

#Операции с наименованиями блюд.

@application.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
def create_dish(request: DishModel, target_menu_id, target_submenu_id):
    return DishRepository.create_dish(
        request.title,
        request.description,
        request.price,
        target_menu_id,
        target_submenu_id,
    )



@application.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def get_dish_item(
    request: Request,
    target_menu_id: int,
    target_submenu_id: int,
    target_dish_id: int,
):
    dish = DishRepository.get_dish_by_id(target_dish_id)
    
    if dish:
        return dish
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='dish not found',
        )
     

@application.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def update_dish(
    request: DishModel,
    target_menu_id: int,
    target_submenu_id: int,
    target_dish_id: int,
):
    return DishRepository.update_dish(
        request.title,
        request.description,
        request.price,
        target_menu_id,
        target_submenu_id,
        target_dish_id,
    )


@application.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def delete_dish(
    request: Request,
    target_menu_id: int,
    target_submenu_id: int,
    target_dish_id: int,
):
    return DishRepository.delete_dish(
        target_menu_id,
        target_submenu_id,
        target_dish_id,
    )


@application.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
def get_dishs_list(
    request: Request,
    target_menu_id: int,
    target_submenu_id: int,
):
    return DishRepository.get_dishs_list(target_menu_id, target_submenu_id)


if __name__ == '__main__':
    uvicorn.run(
        app=application,
        host='127.0.0.1',
        port=8000,
    )