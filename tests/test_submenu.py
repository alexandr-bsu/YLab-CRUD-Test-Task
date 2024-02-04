from src.schemas.menu import MenuSchema, MenuUpdateSchema
from httpx import AsyncClient
from main import app
from fastapi.exceptions import HTTPException
import pytest
from uuid import UUID


@pytest.mark.usefixtures('init_db_fixture')
class TestSubmenu:
    async def test_list_empty_submenus(self, post_menu, menu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()
            menu_db = await menu_services.create(MenuSchema(**post_menu))
            response = await ac.get(f'/menus/{menu_db.id}/submenus/')

            assert response.status_code == 200
            assert response.json() == []
            await menu_services.delete_all()

    async def test_create_submenu(self, post_submenu, post_menu, menu_services, submenu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()
            menu_db = await menu_services.create(MenuSchema(**post_menu))
            payload = MenuSchema(**post_submenu, parent_id=menu_db.id)
            response = await ac.post(f'/menus/{menu_db.id}/submenus/',
                                     json=payload.model_dump())

            submenu_id = response.json()['id']
            submenu_db = await submenu_services.find(submenu_id, menu_db.id)

            assert response.status_code == 201, "incorrect response status code. waiting 201"
            assert submenu_db.id is not None, "submenu's id is absent in DB"
            assert submenu_db.id == UUID(submenu_id), "unexpected submenu's id in DB"
            assert submenu_db.title is not None, "submenu's title is absent in DB"
            assert submenu_db.title == response.json()['title'], "unexpected submenu's id in DB"
            assert submenu_db.title == post_submenu['title'], "submenu's title in request data mutated"
            assert submenu_db.description is not None, "submenu's title is absent in DB"
            assert submenu_db.description == response.json()['description'], "unexpected submenu's id in DB"
            assert submenu_db.description == post_submenu['description'], ("submenu's description in request data "
                                                                           "mutated")
            assert submenu_db.dishes_count == 0, "created submenu's dishes_count value must be equal to 0"

            try:
                await submenu_services.create(MenuSchema(**post_submenu), '00000000-0000-0000-0000-000000000000')
                assert False
            except HTTPException as exc:
                assert exc.status_code == 400
                assert exc.detail == "Cant create submenu in not existing menu"

    async def test_list_submenu(self, post_menu, post_submenu, menu_services, submenu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu = await menu_services.create(MenuSchema(**post_menu))
            submenu = await submenu_services.create(MenuSchema(**post_submenu), menu.id)
            response = await ac.get(f"/menus/{menu.id}/submenus/")

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert response.json() != [], "List of submenus is not displayed"
            assert len(response.json()) != 2, "menu in list of menu"
            assert UUID(response.json()[0]['id']) == submenu.id, "menu was displayed instead of submenu"

            await menu_services.delete_all()

    async def test_get_submenu(self, post_menu, post_submenu, menu_services, submenu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu_db = await menu_services.create(MenuSchema(**post_menu))
            submenu_db = await submenu_services.create(MenuSchema(**post_submenu), menu_db.id)
            response = await ac.get(f"/menus/{menu_db.id}/submenus/{submenu_db.id}")

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert response.json()['id'] is not None, "menu's id is absent in get response"
            assert submenu_db.id == UUID(response.json()['id']), "unexpected submenu's id in get response"
            assert response.json()['title'] is not None, "menu's title is absent in get response"
            assert submenu_db.title == response.json()['title'], "unexpected submenu's id in get response"
            assert response.json()['title'] == post_submenu['title'], "submenu's title in response data is mutated"

            assert response.json()['description'] is not None, "menu's description is absent in get response"
            assert submenu_db.description == response.json()['description'], "unexpected submenu's description in DB"
            assert response.json()['description'] == post_submenu[
                'description'], "submenu's description in response data is mutated"

            response_get_not_existing_submenu = await ac.get(
                f"/menus/3c6b8785-c06f-43b5-b700-1ff5436db9a8/submenus/439d26f9-f4bc-47d1-99de-f2b82f175a68")
            assert response_get_not_existing_submenu.status_code == 404, "incorrect response status code. waiting 404"
            assert response_get_not_existing_submenu.json() == {
                'detail': 'submenu not found'}, "incorrect response detail. waiting: submenu not found"

            await menu_services.delete_all()

    async def test_update_submenu(self, post_menu, post_submenu, update_submenu, menu_services, submenu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu_db = await menu_services.create(MenuSchema(**post_menu))
            submenu_db = submenu_db = await submenu_services.create(MenuSchema(**post_submenu), menu_db.id)
            payload = MenuUpdateSchema(**update_submenu)

            response = await ac.patch(f"/menus/{menu_db.id}/submenus/{submenu_db.id}", json=payload.model_dump())
            update_submenu_db = await submenu_services.find(submenu_db.id, menu_db.id)

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert update_submenu_db.id is not None, "submenu's id is absent in DB"
            assert update_submenu_db.id == submenu_db.id, "submenu's id in DB is changed"

            assert update_submenu_db.title is not None, "menu's title is absent in DB"
            assert update_submenu_db.title == response.json()['title'], "unexpected menu's title in DB"
            assert update_submenu_db.title == update_submenu['title'], "menu's title in DB hasn't changed"

            assert update_submenu_db.description is not None, "menu's description is absent in DB"
            assert update_submenu_db.description == response.json()[
                'description'], "unexpected menu's description in DB"
            assert update_submenu_db.description == update_submenu[
                'description'], "menu's description in DB hasn't changed"

            response_update_not_existing_submenu = await ac.patch(
                f"/menus/{menu_db.id}/submenus/00000000-0000-0000-0000-000000000000",
                json=payload.model_dump())

            assert response_update_not_existing_submenu.status_code == 404, ("incorrect response status code. waiting "
                                                                             "404")
            assert response_update_not_existing_submenu.json() == {
                'detail': 'submenu not found'}, "incorrect response detail. waiting: submenu not found"

        await menu_services.delete_all()

    async def test_delete_submenu(self, post_menu, post_submenu, menu_services, submenu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()
            menu_db = await menu_services.create(MenuSchema(**post_menu))
            submenu_db = await submenu_services.create(MenuSchema(**post_submenu), menu_db.id)

            response = await ac.delete(f"/menus/{menu_db.id}/submenus/{submenu_db.id}")

            assert response.status_code == 200
            assert response.json() == {
                "status": True,
                "message": "The submenu has been deleted"
            }

            try:
                deleted_submenu_result_db = await submenu_services.find(menu_db.id, submenu_db.id)
                assert False
            except HTTPException as exc:
                assert exc.status_code == 404, "incorrect response status code. waiting 404"
                assert exc.detail == "submenu not found", "incorrect response detail. waiting: submenu not found"

            assert await submenu_services.find_all(menu_db.id) == []
        await menu_services.delete_all()
