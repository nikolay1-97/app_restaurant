"""Тесты для хэндлеров crud операций для сущности блюдо"""
from httpx import AsyncClient
from sqlalchemy import insert, select, delete
from tests.conftest import async_session_maker
from app.data_sources.models import Menu_model, Submenu_model, Dish_model

async def test_create_dish(ac: AsyncClient):
        response1 = await ac.post('/api/v1/submenus/3/dishes', json={
            "title": "dish1",
            "description": "my dish1",
            "price": '250.00',
            "from_submenu": 3,
        })
        response2 = await ac.post('/api/v1/submenus/3/dishes', json={
        "title": "dish1",
        "description": "my dish1",
        "price": '250.00',
        "from_submenu": 3,
        })
        response3 = await ac.post('/api/v1/submenus/100/dishes', json={
        "title": "dish2",
        "description": "my dish2",
        "price": '250.00',
        "from_submenu": 100,
        })

        assert response1.status_code == 200
        assert response1.json()['title'] == 'dish1'
        assert response1.json()['description'] == 'my dish1'
        assert response1.json()['price'] == 250
        assert response2.status_code == 400
        assert response2.json()['detail'] == 'Наименование блюда dish1 уже существует'
        assert response3.status_code == 400
        assert response3.json()['detail'] == 'Подменю с id 100 не существует'


async def test_update_dish(create_dish, ac: AsyncClient):
    response1 = await ac.patch('/api/v1/menus/submenus/3/dishes/1', json={
        "title": "new dish1",
        "description": "my new dish1",
        "price": '270.00',
        "from_submenu": 3,
    })
    response2 = await ac.patch('/api/v1/menus/submenus/3/dishes/1', json={
        "title": "dish5",
        "description": "my new dish5",
        "price": '250.00',
        "from_submenu": 3,
    })
    response3 = await ac.patch('/api/v1/menus/submenus/100/dishes/1', json={
        "title": "new dish2",
        "description": "my new dish2",
        "price": '250.00',
        "from_submenu": 100,
    })
    response4 = await ac.patch('/api/v1/menus/submenus/3/dishes/100', json={
        "title": "new dish2",
        "description": "my new dish2",
        "price": '250.00',
        "from_submenu": 3,
    })
    assert response1.status_code == 200
    assert response1.json()['title'] == 'new dish1'
    assert response1.json()['description'] == "my new dish1"
    assert response1.json()['price'] == 270
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'Наименование блюда dish5 уже существует'
    assert response3.status_code == 400
    assert response3.json()['detail'] == 'Подменю с id 100 не существует'
    assert response4.status_code == 400
    assert response4.json()['detail'] == 'dish not found'


async def test_get_dish_item(ac: AsyncClient):
    response1 = await ac.get('/api/v1/dishes/1')
    response2 = await ac.get('/api/v1/dishes/2')
    assert response1.status_code == 200
    assert response1.json()['title'] == 'new dish1'
    assert response1.json()['description'] == "my new dish1"
    assert response1.json()['price'] == 270
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'dish not found'


async def test_get_dish_list(ac: AsyncClient):
    response = await ac.get('/api/v1/dishes')
    assert response.status_code == 200
    assert response.json()['new dish1']['title'] == 'new dish1'
    assert response.json()['new dish1']['description'] == "my new dish1"
    assert response.json()['new dish1']['price'] == 270


async def test_delete_dish(ac: AsyncClient):
    response1 = await ac.delete('/api/v1/dishes/1')
    response2 = await ac.delete('/api/v1/dishes/2')
    async with async_session_maker() as session:
        query = select(Dish_model).filter(Dish_model.c.id == 1)
        dish = await session.execute(query)
        dish = dish.all()
    assert response1.status_code == 200
    assert len(dish) == 0
    assert response2.status_code == 400
    assert response2.json()['detail'] == 'dish not found'