"""Операции с данными для меню, подменю, блюда"""

from fastapi import HTTPException
from starlette import status
from data_sources.models import Menu_model, Submenu_model, Dish_model, connect_db



class MenuRepository:

    SESSION = connect_db()

    @classmethod
    def get_menu_by_name(cls, menu_name: str):
        exists_menu = cls.SESSION.query(Menu_model).filter(
            Menu_model.c.title == menu_name,
            ).one_or_none()
        if exists_menu:
            return exists_menu
        return False
    

    @classmethod
    def get_menu_by_id(cls, menu_id: int):
        exists_menu = cls.SESSION.query(Menu_model).filter(
            Menu_model.c.id == menu_id,
            ).one_or_none()
        if exists_menu:
            return exists_menu
        return False

    @classmethod
    def create_menu(cls, title: str, description: str):
        exists_menu = cls.get_menu_by_name(title)
        if exists_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню {title} уже существует',
            )
        try:
            query = Menu_model.insert().values(title=title, description=description)
            cls.SESSION.execute(query)
            cls.SESSION.commit()
            menu = cls.get_menu_by_name(title)
            return {
                "id": menu[0],
                "title": menu[1],
                "description": menu[2],
            }

        except Exception:
            return {"detail": 'Произошла ошибка при работе с базой данных'}


    @classmethod
    def update_menu(cls, title: str, description: str, menu_id: int):
        exists_menu = cls.get_menu_by_id(menu_id)

        if exists_menu:
            try:
                query = Menu_model.update().where(
                    Menu_model.c.id == menu_id,
                ).values(
                title=title,
                description=description,
                )
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return {
                    "id": menu_id,
                    "title": title,
                    "description": description
                }
            
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="menu not found",
            )
        
    @classmethod
    def delete_menu(cls, target_menu_id: int):
        exists_menu = cls.get_menu_by_id(target_menu_id)
        if exists_menu:
            try:
                submenu_of_dishs_list = cls.SESSION.query(Submenu_model).filter(
                    Submenu_model.c.from_menu == target_menu_id,
                    ).all()
                submenu_id_of_dishs_list = [submenu[0] for submenu in submenu_of_dishs_list]
                
                for id in submenu_id_of_dishs_list:
                    query = Dish_model.delete().where(Dish_model.c.from_submenu == id)
                    cls.SESSION.execute(query)

                query = Submenu_model.delete().where(Submenu_model.c.from_menu == target_menu_id)
                cls.SESSION.execute(query)
                query2 = Menu_model.delete().where(Menu_model.c.id == target_menu_id)
                cls.SESSION.execute(query2)
                cls.SESSION.commit()
                return {"status": True,
                        "message": "The menu has been deleted"
                }

            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'menu not found',
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
                "title": menu_list[i][1],
                "description": menu_list[i][2],
                "count_of_submenu": list_of_count_of_submenu[i],
                "count_of_dishs": list_of_count_of_dish[i],
            }
        return response
        

class SubMenuRepository:

    SESSION = connect_db()

    @classmethod
    def get_submenu_by_name(cls, submenu_name: str):
        exists_submenu = cls.SESSION.query(Submenu_model).filter(
            Submenu_model.c.title == submenu_name,
            ).one_or_none()
        if exists_submenu:
            return exists_submenu
        return False
    
    @classmethod
    def get_submenu_by_id(cls, submenu_id: int):
        exists_submenu = cls.SESSION.query(Submenu_model).filter(
            Submenu_model.c.id == submenu_id,
            ).one_or_none()
        if exists_submenu:
            return exists_submenu
        return False
    
    @classmethod
    def create_submenu(cls, submenu_name: str, description: str, from_menu: int):
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
                title=submenu_name,
                description=description,
                from_menu=from_menu,
            )
            cls.SESSION.execute(query)
            cls.SESSION.commit()
            menu = cls.get_submenu_by_name(submenu_name)
            return {
                "id": menu[0],
                "title": submenu_name,
                "description": description,
            }

        except Exception:
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        

    @classmethod
    def update_submenu(
        cls,
        title: str,
        description: str,
        from_menu: int,
        submenu_id: int,
    ):
        exists_submenu = cls.get_submenu_by_id(submenu_id)
        exists_new_from_menu = MenuRepository.get_menu_by_id(from_menu)
        if not exists_new_from_menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Меню с id {from_menu} не существует',
            )
        if exists_submenu:
            try:
                query = Submenu_model.update().where(
                    Submenu_model.c.id == submenu_id,
                ).values(
                title=title,
                description=description,
                from_menu=from_menu
                )
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return {
                    "id": submenu_id,
                    "title": title,
                    "description": description,
                }
            
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'submenu not found',
            )

    @classmethod
    def delete_submenu(cls, target_submenu_id: int):
        exists_submenu = cls.get_submenu_by_id(target_submenu_id)
        if exists_submenu:
            try:
                query = Dish_model.delete().where(Dish_model.c.from_submenu == target_submenu_id)
                cls.SESSION.execute(query)
                query2 = Submenu_model.delete().where(Submenu_model.c.id == target_submenu_id)
                cls.SESSION.execute(query2)
                cls.SESSION.commit()
                return {"status": True,
                        "message": "The submenu has been deleted",
                }
                    
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'submenu not found',
            )
        
    @classmethod
    def get_submenu_list(cls, from_menu: int):
        response = {}
        submenu_list = cls.SESSION.query(Submenu_model).all()
        list_id_of_submenu = [submenu[0] for submenu in submenu_list]

        for i in range(len(list_id_of_submenu)):
            dish_list = cls.SESSION.query(Dish_model).filter(
                Dish_model.c.from_submenu == list_id_of_submenu[i],
            ).all()

            response[submenu_list[i][1]] = {
                "id": submenu_list[i][0],
                "title": submenu_list[i][1],
                "description": submenu_list[i][2],
                "count_of_dishs": len(dish_list),
            }
        return response


# Операции с наименованием блюд

class DishRepository:

    SESSION = connect_db()

    @classmethod
    def get_dish_by_name(cls, dish_name: str):
        exists_dish = cls.SESSION.query(Dish_model).filter(
            Dish_model.c.title == dish_name,
            ).one_or_none()
        if exists_dish:
            exists_dish = {
                "id": exists_dish[0],
                "title": exists_dish[1],
                "description": exists_dish[2],
                "price": round(exists_dish[3], 2),
            }
            return exists_dish
        return False
    
    @classmethod
    def get_dish_by_id(cls, dish_id: int):
        exists_dish = cls.SESSION.query(Dish_model).filter(
            Dish_model.c.id == dish_id,
            ).one_or_none()
        if exists_dish:
            exists_dish = {
                "id": exists_dish[0],
                "title": exists_dish[1],
                "description": exists_dish[2],
                "price": round(exists_dish[3], 2),
            }
            return exists_dish
        return False
    
    @classmethod
    def create_dish(cls,
                    dish_name: str,
                    description: str,
                    price: str,
                    from_menu: int,
                    from_submenu: int,
    ):
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
                title=dish_name,
                description=description,
                price=float(price),
                from_submenu=from_submenu,
            )
            cls.SESSION.execute(query)
            cls.SESSION.commit()
            return cls.get_dish_by_name(dish_name)

        except Exception:
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        
    @classmethod
    def update_dish(
        cls,
        dish_name: str,
        description: str,
        price: str,
        from_menu: int,
        from_submenu: int,
        dish_id: int,
    ):
        exists_dish = cls.get_dish_by_id(dish_id)
        exists_submenu = SubMenuRepository.get_submenu_by_id(from_submenu)
        if not exists_submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Подменю с id {from_submenu} не существует',
            )

        if exists_dish:
            try:
                query = Dish_model.update().where(
                    Dish_model.c.id == dish_id,
                ).values(
                title=dish_name,
                description=description,
                price=float(price),
                )
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return {
                    "id": dish_id,
                    "title": dish_name,
                    "description": description,
                    "price": round(float(price), 2),
                }
            
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'dish not found',
            )

    @classmethod
    def delete_dish(
        cls,
        target_menu_id: int,
        target_submenu_id: int,
        target_dish_id: int,
    ):
        exists_dish = cls.get_dish_by_id(target_dish_id)
        if exists_dish:
            try:
                query = Dish_model.delete().where(Dish_model.c.id == target_dish_id)
                cls.SESSION.execute(query)
                cls.SESSION.commit()
                return {
                    "status": True,
                    "message": "The dish has been deleted"
                }
                    
            except Exception:
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'dish not found',
            )

    @classmethod
    def get_dishs_list(cls, from_menu: int, from_submenu: int):
        response = {}
        dish_list = cls.SESSION.query(Dish_model).all()
        
        for i in range(len(dish_list)):
            response[dish_list[i][1]] = {
                "id": dish_list[i][0],
                "title": dish_list[i][1],
                "description": dish_list[i][2],
                "price": round(dish_list[i][3], 2),
            }

        return response
