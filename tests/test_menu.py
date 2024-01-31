from src.schemas.menu import MenuSchema, MenuUpdateSchema, MenuResponseSchema
from httpx import AsyncClient
from main import app
from fastapi.exceptions import HTTPException
import pytest
from uuid import UUID


@pytest.mark.usefixtures('init_db_fixture')
class TestMenu:
    async def test_list_empty_menu(self, menu_services):
        await menu_services.delete_all()
        async with AsyncClient(app=app, base_url="http://test") as ac:

            response = await ac.get("/menus/")
            assert response.status_code == 200
            assert response.json() == []

    async def test_create_menu(self, post_menu, menu_services):
        await menu_services.delete_all()

        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = MenuSchema(**post_menu).model_dump()
            response = await ac.post("/menus/", json=payload)
            menu_id = response.json()['id']

            menu_db = await menu_services.find(menu_id)

            assert response.status_code == 201, "incorrect response status code. waiting 201"
            assert menu_db.id is not None, "menu's id is absent in DB"
            assert menu_db.id == UUID(menu_id), "unexpected menu's id in DB"
            assert menu_db.title is not None, "menu's title is absent in DB"
            assert menu_db.title == response.json()['title'], "unexpected menu's id in DB"
            assert menu_db.title == post_menu['title'], "menu's title in request data mutated"
            assert menu_db.description is not None, "menu's title is absent in DB"
            assert menu_db.description == response.json()['description'], "unexpected menu's id in DB"
            assert menu_db.description == post_menu['description'], "menu's description in request data mutated"
            assert menu_db.dishes_count == 0, "created menu's dishes_count value must be equal to 0"
            assert menu_db.submenus_count == 0, "created menu's submenus_count value must be equal to 0"

        await menu_services.delete_all()

    async def test_list_menu(self, post_menu, post_submenu, menu_services, submenu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu = await menu_services.create(MenuSchema(**post_menu))
            submenu = await submenu_services.create(menu.id, MenuSchema(**post_submenu))
            response = await ac.get("/menus/")

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert response.json() != [], "List of menu is not displayed"
            assert len(response.json()) != 2, "Submenu in list of menu"
            assert UUID(response.json()[0]['id']) == menu.id, "Submenu was displayed instead of menu"

            await menu_services.delete_all()

    async def test_get_menu(self, post_menu, menu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu_db = await menu_services.create(MenuSchema(**post_menu))
            response = await ac.get(f"/menus/{menu_db.id}")

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert response.json()['id'] is not None, "menu's id is absent in get response"
            assert menu_db.id == UUID(response.json()['id']), "unexpected menu's id in get response"
            assert response.json()['title'] is not None, "menu's title is absent in get response"
            assert menu_db.title == response.json()['title'], "unexpected menu's id in get response"
            assert response.json()['title'] == post_menu['title'], "menu's title in response data is mutated"

            assert response.json()['description'] is not None, "menu's description is absent in get response"
            assert menu_db.description == response.json()['description'], "unexpected menu's description in DB"
            assert response.json()['description'] == post_menu[
                'description'], "menu's description in response data is mutated"

            assert menu_db.dishes_count == 0, "menu's dishes_count value must be equal to 0 in get response"
            assert menu_db.submenus_count == 0, "menu's submenus_count value must be equal to 0 get response"

            response_get_not_existing_menu = await ac.get(f"/menus/00000000-0000-0000-0000-000000000000")
            assert response_get_not_existing_menu.status_code == 404, "incorrect response status code. waiting 404"
            assert response_get_not_existing_menu.json() == {'detail': 'menu not found'}, "incorrect response detail. waiting: menu not found"

            await menu_services.delete_all()

    async def test_update_menu(self, post_menu, update_menu, menu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu_db = await menu_services.create(MenuSchema(**post_menu))
            payload = MenuUpdateSchema(**update_menu)

            response = await ac.patch(f"/menus/{menu_db.id}", json=payload.model_dump())
            update_menu_db = await menu_services.find(menu_db.id)

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert update_menu_db.id is not None, "menu's id is absent in DB"
            assert update_menu_db.id == menu_db.id, "menu's id in DB is changed"

            assert update_menu_db.title is not None, "menu's title is absent in DB"
            assert update_menu_db.title == response.json()['title'], "unexpected menu's title in DB"
            assert update_menu_db.title == update_menu['title'], "menu's title in DB hasn't changed"

            assert update_menu_db.description is not None, "menu's description is absent in DB"
            assert update_menu_db.description == response.json()['description'], "unexpected menu's description in DB"
            assert update_menu_db.description == update_menu['description'], "menu's description in DB hasn't changed"

            assert menu_db.dishes_count == 0, "menu's dishes_count value changed"
            assert menu_db.submenus_count == 0, "menu's submenus_count value changed"

            response_update_not_existing_menu = await ac.patch(f"/menus/00000000-0000-0000-0000-000000000000",
                                                               json=payload.model_dump())
            assert response_update_not_existing_menu.status_code == 404, "incorrect response status code. waiting 404"
            assert response_update_not_existing_menu.json() == {'detail': 'menu not found'}, "incorrect response detail. waiting: menu not found"

        await menu_services.delete_all()

    async def test_delete_menu(self, post_menu, menu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()
            menu_db = await menu_services.create(MenuSchema(**post_menu))
            response = await ac.delete(f"/menus/{menu_db.id}")

            assert response.status_code == 200
            assert response.json() == {
                "status": True,
                "message": "The menu has been deleted"
            }

            try:
                deleted_menu_result_db = await menu_services.find(menu_db.id)
                assert False
            except HTTPException as exc:
                assert exc.status_code == 404, "incorrect response status code. waiting 404"
                assert exc.detail == "menu not found", "incorrect response detail. waiting: menu not found"

        await menu_services.delete_all()
