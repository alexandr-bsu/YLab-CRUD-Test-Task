from src.schemas.menu import MenuSchema, MenuUpdateSchema, MenuResponseSchema
import pytest
from fastapi.exceptions import HTTPException


@pytest.mark.usefixtures('init_db_fixture')
class TestMenu:
    async def test_list_empty_menu(self, menu_services):
        response = await menu_services.find_all()
        assert response == []

    async def test_create_menu(self, menu_services, post_menu, session_storage):
        payload = MenuSchema(**post_menu)
        response = await menu_services.create(payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description']) == True
        session_storage['menu'] = response.model_dump()

    async def test_list_menu(self, menu_services):
        response = await menu_services.find_all()
        assert response != []

    async def test_get_menu(self, menu_services, session_storage):
        response = await menu_services.find(session_storage['menu']['id'])
        assert MenuResponseSchema(**session_storage['menu']).compare_fields(response.model_dump(),
                                                                            fields=['title', 'description']) == True

    async def test_update_existing_menu(self, menu_services, update_menu, session_storage):
        payload = MenuUpdateSchema(**update_menu)
        response = await menu_services.update(session_storage['menu']['id'], payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description']) == True
        session_storage['menu'] = response.model_dump()

    async def test_get_menu_after_update(self, menu_services, session_storage):
        response = await menu_services.find(session_storage['menu']['id'])
        assert MenuResponseSchema(**session_storage['menu']).compare_fields(response.model_dump(),
                                                                            fields=['title', 'description']) == True

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

    async def test_get_menu_after_delete(self, menu_services, session_storage):
        try:
            response = await menu_services.find(session_storage['menu']['id'])
            assert False
        except HTTPException as exc:
            assert exc.detail == 'menu not found'
