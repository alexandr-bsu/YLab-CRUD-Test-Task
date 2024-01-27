from src.schemas.menu import MenuSchema, MenuUpdateSchema
from httpx import AsyncClient
from main import app
import pytest


@pytest.mark.usefixtures('init_db_fixture')
class TestMenu:
    async def test_list_empty_menu(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/menus/")

            assert response.status_code == 200
            assert response.json() == []

    async def test_create_menu(self, post_menu, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuSchema(**post_menu)
            response = await ac.post("/menus/", json=payload.model_dump())

            assert response.status_code == 201
            assert payload.compare_fields(response.json(), ['title', 'description']) == True
            session_storage['menu'] = response.json()

    async def test_list_menu(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/menus/")

            assert response.status_code == 200
            assert response.json() != []

    async def test_get_menu(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/menus/{session_storage['menu']['id']}")

            assert response.status_code == 200
            assert MenuSchema(**session_storage['menu']).compare_fields(response.json(),
                                                                        fields=['title', 'description']) == True

    async def test_update_existing_menu(self, update_menu, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuUpdateSchema(**update_menu)
            response = await ac.patch(f"/menus/{session_storage['menu']['id']}", json=payload.model_dump())

            assert response.status_code == 200
            assert payload.compare_fields(response.json(), ['title', 'description']) == True

            session_storage['menu'] = response.json()

    async def test_get_menu_after_update(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/menus/{session_storage['menu']['id']}")

            assert response.status_code == 200
            assert MenuSchema(**session_storage['menu']).compare_fields(response.json(),
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

    async def test_get_menu_after_delete(self, session_storage):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/menus/{session_storage['menu']['id']}")

            assert response.status_code == 404
            assert response.json() == {'detail': 'menu not found'}


