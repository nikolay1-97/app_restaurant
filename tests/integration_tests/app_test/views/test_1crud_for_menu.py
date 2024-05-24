"""Тесты хендлеров crud операций для сущности меню."""
from httpx import AsyncClient
from sqlalchemy import insert, select, delete
from tests.conftest import async_session_maker
from app.data_sources.models import Menu_model, Submenu_model, Dish_model


async def test_create_menu(ac: AsyncClient):
    response = await ac.post("/api/v1/menus", json={
        "title": "test_menu_1",
        "description": "my test_menu_1",
    })
    response2 = await ac.post("/api/v1/menus", json={
        "title": "test_menu_1",
        "description": "my test_menu_1",
    })
    assert response.status_code == 200
    assert response.json()['title'] == 'test_menu_1'
    assert response.json()["description"] == "my test_menu_1"
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'Меню test_menu_1 уже существует'


async def test_update_menu(create_menu, ac: AsyncClient):
    response = await ac.patch("/api/v1/menus/1", json={
        "title": "new_test_menu1",
        "description": "my new_test_menu_1",
    })
    response2 = await ac.patch("/api/v1/menus/1", json={
        "title": "menu2",
        "description": "my menu2",
    })
    response3 = await ac.patch("/api/v1/menus/2", json={
        "title": "new_test_menu2",
        "description": "my new_test_menu_1",
    })
    assert response.status_code == 200
    assert response.json()['title'] == "new_test_menu1"
    assert response.json()["description"] == "my new_test_menu_1"
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'Меню menu2 уже существует'
    assert response3.status_code == 400
    assert response3.json()['detail'] == "menu not found"


async def test_get_menu_list(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = insert(Submenu_model).values(
            title='submenu1',
            description='my submenu1',
            from_menu=1,
        )
        await session.execute(stmt)
        await session.commit()
    response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json()["new_test_menu1"]['title'] == "new_test_menu1"
    assert response.json()["new_test_menu1"]["description"] == "my new_test_menu_1"
    assert response.json()["new_test_menu1"]["count_of_submenu"] == 1


async def test_get_menu_item(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = insert(Dish_model).values(
            id=1,
            title='dish1',
            description='my dish1',
            price=250.00,
            from_submenu=1,
        )
        await session.execute(stmt)
        await session.commit()
    response = await ac.get('/api/v1/menus/1')
    response2 = await ac.get('/api/v1/menus/2')
    assert response.status_code == 200
    assert response.json()['title'] == "new_test_menu1"
    assert response.json()["description"] == "my new_test_menu_1"
    assert response.json()["count_of_submenu"] == 1
    assert response.json()["count_of_dishs"] == 1
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'menu not found'


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete('/api/v1/menus/1')
    resp = await ac.get('/api/v1/menus/1')
    async with async_session_maker() as session:
        query1 = select(Submenu_model).filter(Submenu_model.c.title == 'submenu1')
        query2 = select(Dish_model).filter(Dish_model.c.title == 'dish1')
        submenu = await session.execute(query1)
        submenu = submenu.all()
        dish = await session.execute(query2)
        dish = dish.all()
    assert len(submenu) == 0
    assert len(dish) == 0
    assert response.status_code == 200
    assert resp.status_code == 400
    assert resp.json()['detail'] == 'menu not found'
    