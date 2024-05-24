"""Тесты для хендлеров crud операций для сущности подменю"""
from httpx import AsyncClient
from sqlalchemy import insert, select, delete
from tests.conftest import async_session_maker
from app.data_sources.models import Menu_model, Submenu_model, Dish_model
from app.data_sources.storages.submenu_reposytory import SubMenuRepository

async def test_create_submenu(ac: AsyncClient):
    #async with async_session_maker() as session:
        #stmt = insert(Menu_model).values(
            #id=1,
            #title='menu1',
            #description='my menu1',
        #)
        #await session.execute(stmt)
        #await session.commit()
    response = await ac.post('/api/v1/menus/5/submenus', json={
        "title": "test_submenu1",
        "description": "my test_submenu1",
        "from_menu": 5,
    })
    async with async_session_maker() as session:
        id_menu = await SubMenuRepository.get_id_by_name("submenu1", session)
    response2 = await ac.post("/api/v1/menus/5/submenus", json={
        "title": "test_submenu1",
        "description": "my test_submenu1",
        "from_menu": 5,
    })
    response3 = await ac.post("/api/v1/menus/100/submenus", json={
        "title": "test_submenu2",
        "description": "my test_submenu2",
        "from_menu": 100,
    })
    assert response.status_code == 200
    assert response.json()['title'] == 'test_submenu1'
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'Подменю test_submenu1 уже существует'
    assert response3.status_code == 400
    assert response3.json()['detail'] == 'Меню с id 100 не существует'
    #assert id_menu == 100


async def test_update_submenu(create_submenu, ac: AsyncClient):
    response = await ac.patch('/api/v1/menus/5/submenus/2', json={
        "title": "new test_submenu1",
        "description": "my new test_submenu1",
        "from_menu": 5,
    })
    response2 = await ac.patch('/api/v1/menus/5/submenus/2', json={
        "title": "submenu2",
        "description": "new test_submenu2",
        "from_menu": 5,
    })
    response3 = await ac.patch('/api/v1/menus/100/submenus/2', json={
        "title": "new test_submenu2",
        "description": "my new test_submenu2",
        "from_menu": 5,
    })
    response4 = await ac.patch('/api/v1/menus/5/submenus/100', json={
        "title": "new test_submenu2",
        "description": "my new test_submenu2",
        "from_menu": 5,
    })
    assert response.status_code == 200
    assert response.json()['title'] == 'new test_submenu1'
    assert response.json()['description'] == 'my new test_submenu1'
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'Подменю submenu2 уже существует'
    assert response3.status_code == 400
    assert response3.json()['detail'] == 'Меню с id 100 не существует'
    assert response4.status_code == 400
    assert response4.json()['detail'] == 'submenu not found'


async def test_get_submenu_list(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = insert(Dish_model).values(
            id=1,
            title='dish1',
            description='my dish1',
            price=250.00,
            from_submenu=2,
        )
        await session.execute(stmt)
        await session.commit()
    response = await ac.get('/api/v1/submenus')
    assert response.status_code == 200
    assert response.json()['new test_submenu1']['title'] == 'new test_submenu1'
    assert response.json()['new test_submenu1']['description'] == 'my new test_submenu1'
    assert response.json()['new test_submenu1']['count_of_dishs'] == 1


async def test_get_submenu_item(ac: AsyncClient):
    response = await ac.get('/api/v1/submenus/2')
    response2 = await ac.get('/api/v1/submenus/5')
    assert response.status_code == 200
    assert response.json()['title'] == 'new test_submenu1'
    assert response.json()['description'] == 'my new test_submenu1'
    assert response.json()['count_of_dishs'] == 1
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'submenu not found'


async def test_delete_submenu(ac: AsyncClient):
    response = await ac.delete('/api/v1/submenus/2')
    response2 = await ac.delete('/api/v1/submenus/5') 
    async with async_session_maker() as session:
        query1 = select(Submenu_model).filter(Submenu_model.c.title == 'new test_submenu1')
        submenu = await session.execute(query1)
        submenu = submenu.all()
        query2 = select(Dish_model).filter(Dish_model.c.title == 'dish1')
        dish = await session.execute(query2)
        dish = dish.all()
        #stmt = Menu_model.delete().where(Menu_model.c.id == 1)
        #await session.execute(stmt)
        await session.commit()
    assert response.status_code == 200
    assert len(submenu) == 0
    assert len(dish) == 0
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'submenu not found'
