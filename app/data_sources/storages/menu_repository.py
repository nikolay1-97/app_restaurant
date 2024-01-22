"""Операции с данными для меню, подменю, блюда"""

from fastapi import HTTPException
from starlette import status
from data_sources.models import Menu_model, Submenu_model, Dish_model, connect_db



class MenuRepository:

    SESSION = connect_db()

    @classmethod
    def get_menu_by_name(cls, menu_name: str):
        exists_menu = cls.SESSION.query(Menu_model).filter(
            Menu_model.c.name == menu_name,
            ).one_or_none()
        if exists_menu:
            return exists_menu
        return False
    

    @classmethod
    def get_menu_by_id(cls, id: int):
        exists_menu = cls.SESSION.query(Menu_model).filter(
            Menu_model.c.id == id,
            ).one_or_none()
        if exists_menu:
            return exists_menu
        return False

    @classmethod
    def create_menu(cls, menu_name: str):
        exists_menu = cls.get_menu_by_name(menu_name)
        if exists_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню {menu_name} уже существует',
            )
        try:
            query = Menu_model.insert().values(name=menu_name)
            cls.SESSION.execute(query)
            cls.SESSION.commit()
            return {"detail": f'Позиция успешно добавлена. Имя меню: {menu_name}'}

        except Exception:
            return {"detail": 'Произошла ошибка при работе с базой данных'}


    @classmethod
    def update_menu(cls, menu_name: str, new_menu_name: str):
        exists_menu = cls.get_menu_by_name(menu_name)
        exists_new_menu_name = cls.get_menu_by_name(new_menu_name)
        if exists_new_menu_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Позиция {new_menu_name} уже существует',
            )

        if exists_menu:
            try:
                query = Menu_model.update().where(
                    Menu_model.c.name == menu_name,
                ).values(
                name=new_menu_name,
                )
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return {"detail": f'Данные успешно обновлены. Имя меню: {new_menu_name}'}
            
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Позиция {menu_name} не найдена',
            )
        
    @classmethod
    def delete_menu(cls, menu_name: str):
        exists_menu = cls.get_menu_by_name(menu_name)
        if exists_menu:
            menu_id = exists_menu[0]
            try:
                submenu_of_dishs_list = cls.SESSION.query(Submenu_model).filter(
                    Submenu_model.c.from_menu == menu_id,
                    ).all()
                submenu_id_of_dishs_list = [submenu[0] for submenu in submenu_of_dishs_list]
                
                for id in submenu_id_of_dishs_list:
                    query = Dish_model.delete().where(Dish_model.c.from_submenu == id)
                    cls.SESSION.execute(query)

                query = Submenu_model.delete().where(Submenu_model.c.from_menu == menu_id)
                cls.SESSION.execute(query)
                query2 = Menu_model.delete().where(Menu_model.c.name == menu_name)
                cls.SESSION.execute(query2)
                cls.SESSION.commit()
                return {"detail": f'Позиция меню {menu_name} и позиции подменю с ключем {menu_id}  и \
                    соответствующие позиции блюд успешно удалены',
                }

            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Наименование меню {menu_name} не найдено',
            )
        
    @classmethod
    def get_menu_list(cls):

        list_of_count_of_submenu = []
        list_of_count_of_dish = []
        list_of_submenu = []
        menu_list = cls.SESSION.query(Menu_model).all()
        menu_id_list = [menu[0] for menu in menu_list]
        response = {}

        for id in menu_id_list:
            submenu_list = cls.SESSION.query(Submenu_model).filter(
                Submenu_model.c.from_menu == id,
                ).all()
            list_of_count_of_submenu.append(len(submenu_list))
            list_of_submenu.append(submenu_list)
            
        for lst in list_of_submenu:
            count = 0
            for submenu in lst:
                dish_list = cls.SESSION.query(Dish_model).filter(
                    Dish_model.c.from_submenu == submenu[0],
                ).all()
                count += len(dish_list)
            list_of_count_of_dish.append(count)

        for i in range(len(menu_list)):
            response[menu_list[i][1]] = {
                "id": menu_list[i][0],
                "name": menu_list[i][1],
                "count_of_submenu": list_of_count_of_submenu[i],
                "count_of_dish": list_of_count_of_dish[i],
            }
        return response
        

class SubMenuRepository:

    SESSION = connect_db()

    @classmethod
    def get_submenu_by_name(cls, submenu_name: str):
        exists_submenu = cls.SESSION.query(Submenu_model).filter(
            Submenu_model.c.name == submenu_name,
            ).one_or_none()
        if exists_submenu:
            return exists_submenu
        return False
    
    @classmethod
    def get_submenu_by_id(cls, id: int):
        exists_submenu = cls.SESSION.query(Submenu_model).filter(
            Submenu_model.c.id == id,
            ).one_or_none()
        if exists_submenu:
            return exists_submenu
        return False
    
    @classmethod
    def create_submenu(cls, submenu_name: str, from_menu: int):
        exists_submenu = cls.get_submenu_by_name(submenu_name)
        if exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю {submenu_name} уже существует',
            )
        exists_menu = MenuRepository.get_menu_by_id(from_menu)

        if not exists_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню с id {from_menu} не существует',
            )
        try:
            query = Submenu_model.insert().values(
                name=submenu_name,
                from_menu=from_menu,
            )
            cls.SESSION.execute(query)
            cls.SESSION.commit()
            return {"detail": f'Позиция успешно добавлена. Имя меню: {submenu_name}'}

        except Exception:
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        

    @classmethod
    def update_submenu(
        cls,
        submenu_name: str,
        new_submenu_name: str,
        new_from_menu: int,
    ):
        exists_submenu = cls.get_submenu_by_name(submenu_name)
        exists_new_submenu_name = cls.get_submenu_by_name(new_submenu_name)
        exists_new_from_menu = MenuRepository.get_menu_by_id(new_from_menu)
        if not exists_new_from_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню с id {new_from_menu} не существует',
            )
        if exists_new_submenu_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю {new_submenu_name} уже существует',
            )
        if exists_submenu:
            try:
                query = Submenu_model.update().where(
                    Submenu_model.c.name == submenu_name,
                ).values(
                name=new_submenu_name,
                from_menu=new_from_menu
                )
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return {"detail": f'Данные успешно обновлены. Имя меню: {new_submenu_name}'}
            
            except Exception:
                return {"detail": f'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю {submenu_name} не найдено',
            )

    @classmethod
    def delete_submenu(cls, submenu_name: str):
        exists_submenu = cls.get_submenu_by_name(submenu_name)
        if exists_submenu:
            submenu_id = exists_submenu[0]
            try:
                query = Dish_model.delete().where(Dish_model.c.from_submenu == submenu_id)
                cls.SESSION.execute(query)
                query2 = Submenu_model.delete().where(Submenu_model.c.name == submenu_name)
                cls.SESSION.execute(query2)
                cls.SESSION.commit()
                return {"detail": f'Позиция подменю {submenu_name} и \
                    позиции наименований блюд с ключем {submenu_id} успешно удалены',
                }
                    
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Наименование подменю {submenu_name} не найдено',
            )
        
    @classmethod
    def get_submenu_list(cls):
        response = {}
        submenu_list = cls.SESSION.query(Submenu_model).all()
        list_id_of_submenu = [submenu[0] for submenu in submenu_list]

        for i in range(len(list_id_of_submenu)):
            dish_list = cls.SESSION.query(Dish_model).filter(
                Dish_model.c.from_submenu == list_id_of_submenu[i],
            ).all()

            response[submenu_list[i][1]] = {
                "id": submenu_list[i][0],
                "name": submenu_list[i][1],
                "from_menu": submenu_list[i][2],
                "count_of_dishs": len(dish_list),
            }
        return response


# Операции с наименованием блюд

class DishRepository:

    SESSION = connect_db()

    @classmethod
    def get_dish_by_name(cls, dish_name: str):
        exists_dish = cls.SESSION.query(Dish_model).filter(
            Dish_model.c.name == dish_name,
            ).one_or_none()
        if exists_dish:
            exists_dish = {
                "id": exists_dish[0],
                "name": exists_dish[1],
                "price": round(exists_dish[2], 2),
                "from_submenu": exists_dish[3],
            }
            return exists_dish
        return False
    
    @classmethod
    def create_dish(cls, dish_name: str, price: float, from_submenu: int):
        exists_dish = cls.get_dish_by_name(dish_name)
        if exists_dish:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Наименование блюда {dish_name} уже существует',
            )
        exists_submenu = SubMenuRepository.get_submenu_by_id(from_submenu)

        if not exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю с id {from_submenu} не существует',
            )
        
        try:
            query = Dish_model.insert().values(
                name=dish_name,
                price=price,
                from_submenu=from_submenu,
            )
            cls.SESSION.execute(query)
            cls.SESSION.commit()
            return {"detail": f'Позиция успешно добавлена. Имя наименования блюда: {dish_name}'}

        except Exception:
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        
    @classmethod
    def update_dish(
        cls,
        dish_name: str,
        new_dish_name: str,
        new_price: float,
        new_from_submenu: str,
    ):
        exists_dish = cls.get_dish_by_name(dish_name)
        exists_new_dish_name = cls.get_dish_by_name(new_dish_name)
        exists_submenu = SubMenuRepository.get_submenu_by_id(new_from_submenu)
        if not exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю с id {new_from_submenu} не существует',
            )

        if exists_new_dish_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Наименование блюда {new_dish_name} уже существует',
            )
        if exists_dish:
            try:
                query = Dish_model.update().where(
                    Dish_model.c.name == dish_name,
                ).values(
                name=new_dish_name,
                price=new_price,
                from_submenu=new_from_submenu,
                )
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return {"detail": f'Данные успешно обновлены. Имя наименования блюда: {new_dish_name}'}
            
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Наименование блюда {dish_name} не найдено',
            )

    @classmethod
    def delete_dish(cls, dish_name: str):
        exists_dish = cls.get_dish_by_name(dish_name)
        if exists_dish:
            try:
                query = Dish_model.delete().where(Dish_model.c.name == dish_name)
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return {"detail": f'Позиция наименования блюда {dish_name} успешно удалена'}
                    
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Наименование блюда {dish_name} не найдено',
            )

    @classmethod
    def get_dishs_list(cls):
        response = {}
        dish_list = cls.SESSION.query(Dish_model).all()
        
        for i in range(len(dish_list)):
            response[dish_list[i][1]] = {
                "id": dish_list[i][0],
                "name": dish_list[i][1],
                "price": round(dish_list[i][2], 2),
                "from_submenu": dish_list[i][3],
            }

        return response
