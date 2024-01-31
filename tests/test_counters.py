from src.schemas.menu import MenuSchema, MenuUpdateSchema, MenuResponseSchema, SubmenuResponseSchema
from src.schemas.dish import DishSchema, DishUpdateSchema

from httpx import AsyncClient
from main import app
import pytest


@pytest.mark.usefixtures('init_db_fixture')
class TestCounters:

    # Полный тест меню в tests/test_menu.py
    async def test_create_menu(self, post_menu, menu_services, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuSchema(**post_menu)
            response = await ac.post("/menus/", json=payload.model_dump())

            menu_id = response.json()['id']
            menu_db = await menu_services.find(menu_id)

            assert response.status_code == 201
            assert response.json()['title'] == post_menu['title']
            assert response.json()['description'] == post_menu['description']

            session_storage['menu'] = response.json()

    # Полный тест меню в tests/test_menu.py
    async def test_create_submenu(self, post_submenu, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuSchema(**post_submenu, parent_id=session_storage["menu"]["id"])
            response = await ac.post(f'/menus/{session_storage["menu"]["id"]}'
                                     f'/submenus/',
                                     json=payload.model_dump())

            assert response.status_code == 201
            assert payload.compare_fields(response.json(), ['title', 'description'])

            session_storage['submenu'] = response.json()

    async def test_create_dish_1(self, post_dish_1, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = DishSchema(**post_dish_1, menu_id=session_storage["submenu"]["id"])
            response = await ac.post(
                f'/menus/{session_storage["menu"]["id"]}'
                f'/submenus/{session_storage["submenu"]["id"]}'
                f'/dishes/',
                json=payload.model_dump()
            )

            assert response.status_code == 201
            assert payload.compare_fields(response.json(), ['title', 'description', 'price'])

            session_storage['dish_1'] = response.json()

    async def test_create_dish_2(self, post_dish_2, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = DishSchema(**post_dish_2, menu_id=session_storage["submenu"]["id"])
            response = await ac.post(
                f'/menus/{session_storage["menu"]["id"]}'
                f'/submenus/{session_storage["submenu"]["id"]}'
                f'/dishes/',
                json=payload.model_dump()
            )

            assert response.status_code == 201
            assert payload.compare_fields(response.json(), ['title', 'description', 'price'])

            session_storage['dish_2'] = response.json()

    async def test_menu_counters(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f'/menus/{session_storage["menu"]["id"]}')

            assert response.status_code == 200
            assert response.json()['dishes_count'] == 2
            assert response.json()['submenus_count'] == 1
            assert MenuResponseSchema(**session_storage['menu']).compare_fields(response.json(),
                                                                                fields=['title', 'description']) == True

    async def test_submenu_counters(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f'/menus/{session_storage["menu"]["id"]}'
                f'/submenus/{session_storage["submenu"]["id"]}')

            assert response.status_code == 200
            assert response.json()['dishes_count'] == 2
            assert SubmenuResponseSchema(**session_storage['submenu']).compare_fields(response.json(),
                                                                                      fields=['title',
                                                                                              'description']) == True

    async def test_delete_submenu(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(
                f"/menus/{session_storage['menu']['id']}/submenus/{session_storage['submenu']['id']}"
            )

            assert response.status_code == 200
            assert response.json() == {
                "status": True,
                "message": "The submenu has been deleted"
            }

            session_storage['submenu']['id'] = '00000000-0000-0000-0000-000000000000'

    async def test_list_submenus_after_delete(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f'/menus/{session_storage["menu"]["id"]}/submenus/')

            assert response.status_code == 200
            assert response.json() == []

    async def test_list_dishes_after_delete_submenu(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"/menus/{session_storage['menu']['id']}"
                f"/submenus/{session_storage['submenu']['id']}"
                f"/dishes/"
            )

            assert response.status_code == 200
            assert response.json() == []

    async def test_menu_counters_after_delete_submenu(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f'/menus/{session_storage["menu"]["id"]}')

            assert response.status_code == 200
            assert response.json()['dishes_count'] == 0
            assert response.json()['submenus_count'] == 0
            assert MenuResponseSchema(**session_storage['menu']).compare_fields(response.json(),
                                                                                fields=['title', 'description']) == True

    async def test_delete_menu(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(f"/menus/{session_storage['menu']['id']}")

            assert response.status_code == 200
            assert response.json() == {
                "status": True,
                "message": "The menu has been deleted"
            }

            session_storage['menu']['id'] = '00000000-0000-0000-0000-000000000000'

    async def test_list_empty_menu_after_delete(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/menus/")

            assert response.status_code == 200
            assert response.json() == []
