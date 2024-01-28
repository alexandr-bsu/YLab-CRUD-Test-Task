from src.schemas.menu import MenuSchema, MenuUpdateSchema, MenuResponseSchema
from httpx import AsyncClient
from main import app
import pytest


@pytest.mark.usefixtures('init_db_fixture')
class TestSubmenu:
    async def test_create_menu(self, post_menu, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuSchema(**post_menu)
            response = await ac.post("/menus/", json=payload.model_dump())

            assert response.status_code == 201
            assert payload.compare_fields(response.json(), ['title', 'description']) == True
            session_storage['menu'] = response.json()

    async def test_list_empty_submenus(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f'/menus/{session_storage["menu"]["id"]}/submenus/')

            assert response.status_code == 200
            assert response.json() == []

    async def test_create_submenu(self, post_submenu, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuSchema(**post_submenu, parent_id=session_storage["menu"]["id"])
            response = await ac.post(f'/menus/{session_storage["menu"]["id"]}/submenus/',
                                     json=payload.model_dump())

            assert response.status_code == 201
            assert payload.compare_fields(response.json(), ['title', 'description'])

            session_storage['submenu'] = response.json()

    async def test_list_submenus_after_create(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f'/menus/{session_storage["menu"]["id"]}/submenus/')

            assert response.status_code == 200
            assert response.json() != []

    async def test_get_submenu(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f'/menus/{session_storage["menu"]["id"]}/submenus/{session_storage["submenu"]["id"]}')

            assert response.status_code == 200
            assert MenuResponseSchema(**session_storage['submenu']).compare_fields(response.json(),
                                                                           fields=['title', 'description']) == True

    async def test_update_submenu(self, update_submenu, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuUpdateSchema(**update_submenu)
            response = await ac.patch(
                f"/menus/{session_storage['menu']['id']}/submenus/{session_storage['submenu']['id']}",
                json=payload.model_dump())

            assert response.status_code == 200
            assert payload.compare_fields(response.json(), ['title', 'description']) == True
            session_storage['submenu'] = response.json()

    async def test_get_submenu_after_update(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f"/menus/{session_storage['menu']['id']}/submenus/{session_storage['submenu']['id']}"
            )

            assert response.status_code == 200
            assert MenuResponseSchema(**session_storage['submenu']).compare_fields(response.json(),
                                                                           fields=['title', 'description']) == True

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

    async def test_get_submenu_after_delete(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                f'/menus/{session_storage["menu"]["id"]}/submenus/{session_storage["submenu"]["id"]}')

            assert response.status_code == 404
            assert response.json() == {'detail': 'submenu not found'}

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
