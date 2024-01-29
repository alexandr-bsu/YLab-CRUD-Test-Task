from src.schemas.menu import MenuSchema, MenuUpdateSchema, MenuResponseSchema
from fastapi.exceptions import HTTPException
import pytest


@pytest.mark.usefixtures('init_db_fixture')
class TestSubmenu:
    async def test_create_menu(self, menu_services, post_menu, session_storage):
        payload = MenuSchema(**post_menu)
        response = await menu_services.create(payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description']) == True
        session_storage['menu'] = response.model_dump()

    async def test_list_empty_submenus(self, submenu_services, session_storage):
        response = await submenu_services.find_all(session_storage['menu']['id'])
        assert response == []

    async def test_create_submenu(self, submenu_services, post_submenu, session_storage):
        payload = MenuSchema(**post_submenu)
        response = await submenu_services.create(session_storage["menu"]["id"], payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description'])
        session_storage['submenu'] = response.model_dump()

    async def test_list_submenus_after_create(self, submenu_services, session_storage):
        response = await submenu_services.find_all(session_storage['menu']['id'])
        assert response != []

    async def test_get_submenu(self, submenu_services, session_storage):
        response = await submenu_services.find(session_storage['menu']['id'], session_storage['submenu']['id'])
        assert MenuResponseSchema(**session_storage['submenu']).compare_fields(response.model_dump(),
                                                                               fields=['title', 'description']) == True

    async def test_update_submenu(self, submenu_services, update_submenu, session_storage):
        payload = MenuUpdateSchema(**update_submenu)
        response = await submenu_services.update(session_storage['menu']['id'], session_storage['submenu']['id'], payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description']) == True
        session_storage['submenu'] = response.model_dump()

    async def test_get_submenu_after_update(self, submenu_services, session_storage):
        response = await submenu_services.find(session_storage['menu']['id'], session_storage['submenu']['id'])
        assert MenuResponseSchema(**session_storage['submenu']).compare_fields(response.model_dump(),
                                                                               fields=['title', 'description']) == True

    async def test_delete_submenu(self, submenu_services, session_storage):
        response = await submenu_services.delete(session_storage['submenu']['id'])
        assert response == {
            "status": True,
            "message": "The submenu has been deleted"
        }

        session_storage['submenu']['id'] = '00000000-0000-0000-0000-000000000000'

    async def test_list_submenus_after_delete(self, submenu_services, session_storage):
        response = await submenu_services.find_all(session_storage['menu']['id'])
        assert response == []

    async def test_get_submenu_after_delete(self, submenu_services, session_storage):
        try:
            response = await submenu_services.find(session_storage['menu']['id'], session_storage['submenu']['id'])
            assert False
        except HTTPException as exc:
            assert exc.detail == 'submenu not found'

    async def test_delete_menu(self, menu_services, session_storage):
        response = await menu_services.delete(session_storage['menu']['id'])
        assert response == {
            "status": True,
            "message": "The menu has been deleted"
        }

        session_storage['menu']['id'] = '00000000-0000-0000-0000-000000000000'

    async def test_list_empty_menu_after_delete(self, menu_services):
        response = await menu_services.find_all()
        assert response == []
