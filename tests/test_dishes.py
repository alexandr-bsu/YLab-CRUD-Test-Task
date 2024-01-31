from src.schemas.dish import DishSchema, DishUpdateSchema, DishResponseSchema
from src.schemas.menu import MenuSchema
from httpx import AsyncClient
from main import app
import pytest


@pytest.mark.usefixtures('init_db_fixture')
class TestDish:
    async def test_create_menu(self, post_menu, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuSchema(**post_menu)
            response = await ac.post("/menus/", json=payload.model_dump())

            assert response.status_code == 201
            assert payload.compare_fields(response.json(), ['title', 'description']) == True
            session_storage['menu'] = response.json()

    async def test_create_submenu(self, post_submenu, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuSchema(**post_submenu, parent_id=session_storage["menu"]["id"])
            response = await ac.post(f'/menus/{session_storage["menu"]["id"]}/submenus/',
                                     json=payload.model_dump())

            assert response.status_code == 201
            assert payload.compare_fields(response.json(), ['title', 'description'])

            session_storage['submenu'] = response.json()

    async def test_list_empty_dishes(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f'/menus/{session_storage["menu"]["id"]}'
                f'/submenus/{session_storage["submenu"]["id"]}'
                f'/dishes/'
            )

            assert response.status_code == 200
            assert response.json() == []

    async def test_create_dish(self, post_dish_1, session_storage):
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

            session_storage['dish'] = response.json()

    async def test_list_dishes_after_create(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f'/menus/{session_storage["menu"]["id"]}'
                f'/submenus/{session_storage["submenu"]["id"]}'
                f'/dishes/'
            )

            assert response.status_code == 200
            assert response.json() != []

    async def test_get_dish(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f'/menus/{session_storage["menu"]["id"]}'
                f'/submenus/{session_storage["submenu"]["id"]}'
                f'/dishes/{session_storage["dish"]["id"]}')

            assert response.status_code == 200
            assert DishResponseSchema(**session_storage['dish']).compare_fields(response.json(),
                                                                        fields=['title', 'description',
                                                                                'price']) == True

    async def test_update_dish(self, update_dish_1, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = DishUpdateSchema(**update_dish_1)
            response = await ac.patch(
                f"/menus/{session_storage['menu']['id']}"
                f"/submenus/{session_storage['submenu']['id']}"
                f"/dishes/{session_storage['dish']['id']}",
                json=payload.model_dump())

            assert response.status_code == 200
            assert payload.compare_fields(response.json(), ['title', 'description', 'price']) == True
            session_storage['dish'] = response.json()

    async def test_get_dish_after_update(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f'/menus/{session_storage["menu"]["id"]}'
                f'/submenus/{session_storage["submenu"]["id"]}'
                f'/dishes/{session_storage["dish"]["id"]}')

            assert response.status_code == 200
            assert DishResponseSchema(**session_storage['dish']).compare_fields(response.json(),
                                                                        fields=['title', 'description',
                                                                                'price']) == True

    async def test_delete_dish(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(
                f"/menus/{session_storage['menu']['id']}"
                f"/submenus/{session_storage['submenu']['id']}"
                f"/dishes/{session_storage['dish']['id']}"
            )

            assert response.status_code == 200
            assert response.json() == {
                "status": True,
                "message": "The dish has been deleted"
            }

            session_storage['dish']['id'] = '00000000-0000-0000-0000-000000000000'

    async def test_list_dishes_after_delete(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"/menus/{session_storage['menu']['id']}"
                f"/submenus/{session_storage['submenu']['id']}"
                f"/dishes/"
            )

            assert response.status_code == 200
            assert response.json() == []

    async def test_get_dish_after_delete(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f'/menus/{session_storage["menu"]["id"]}'
                f'/submenus/{session_storage["submenu"]["id"]}'
                f'/dishes/{session_storage["dish"]["id"]}')

            assert response.status_code == 404
            assert response.json() == {'detail': 'dish not found'}

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



