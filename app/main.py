"""Файл запуска приложения"""

from fastapi import FastAPI
from fastapi import HTTPException, Request
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


@application.post('/create_menu')
def create_menu(request: MenuModel):
    return MenuRepository.create_menu(request.menu_name)


@application.patch('/update_menu')
def update_menu(request: MenuModelUpdate):
    return MenuRepository.update_menu(
        request.menu_name,
        request.new_menu_name,
    )


@application.get('/get_menu_item/{menu_name}')
def get_menu_by_name(request: Request, menu_name: str):
    menu = MenuRepository.get_menu_by_name(menu_name)
    if menu:
        return {'id': menu[0], 'name': menu[1]}
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню {menu_name} не существует',
        )
    
@application.delete('/delete_menu/{menu_name}')
def delete_menu(request: Request, menu_name: str):
    return MenuRepository.delete_menu(menu_name)


@application.get('/get_menu_list')
def get_menu_list(request: Request):
    response = MenuRepository.get_menu_list()
    return response

# Операции с подменю.

@application.post('/create_submenu')
def create_submenu(request: SubmenuModel):
    return SubMenuRepository.create_submenu(
        request.submenu_name,
        request.from_menu,
    )

@application.get('/get_submenu_item/{submenu_name}')
def get_submenu_item(request: Request, submenu_name: str):
    submenu = SubMenuRepository.get_submenu_by_name(submenu_name)
    
    if submenu:
        return {'id': submenu[0],
                'name': submenu[1],
                'from_menu': submenu[2],
        }
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю {submenu_name} не существует',
        )
    

@application.patch('/update_submenu')
def update_submenu(request: SubmenuModelUpdate):
    return SubMenuRepository.update_submenu(
        request.submenu_name,
        request.submenu_new_name,
        request.new_from_menu
    )


@application.delete('/delete_submenu/{submenu_name}')
def delete_submenu(request: Request, submenu_name: str):
    return SubMenuRepository.delete_submenu(submenu_name)


@application.get('/get_submenu_list')
def get_submenu_list(request: Request):
    return SubMenuRepository.get_submenu_list()

#Операции с наименованиями блюд.

@application.post('/create_dish')
def create_dish(request: DishModel):
    return DishRepository.create_dish(
        request.name,
        request.price,
        request.from_submenu,
    )


@application.get('/get_dish_item/{dish_name}')
def get_dish_item(request: Request, dish_name: str):
    dish = DishRepository.get_dish_by_name(dish_name)
    
    if dish:
        return dish
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Наименования блюда {dish_name} не существует',
        )
     

@application.patch('/update_dish')
def update_dish(request: DishModelUpdate):
    return DishRepository.update_dish(
        request.name,
        request.new_name,
        request.new_price,
        request.new_from_submenu,
    )


@application.delete('/delete_dish/{dish_name}')
def delete_dish(request: Request, dish_name: str):
    return DishRepository.delete_dish(dish_name)


@application.get('/get_dishs_list')
def get_dishs_list(request: Request):
    return DishRepository.get_dishs_list()


if __name__ == '__main__':
    uvicorn.run(
        app=application,
        host='127.0.0.1',
        port=8080,
    )