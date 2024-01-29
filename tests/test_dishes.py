from src.schemas.dish import DishSchema, DishUpdateSchema, DishResponseSchema
from src.schemas.menu import MenuSchema
import pytest
from fastapi.exceptions import HTTPException


@pytest.mark.usefixtures('init_db_fixture')
class TestDish:
    async def test_create_menu(self, menu_services, post_menu, session_storage):
        payload = MenuSchema(**post_menu)
        response = await menu_services.create(payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description']) == True
        session_storage['menu'] = response.model_dump()

    async def test_create_submenu(self, submenu_services, post_submenu, session_storage):
        payload = MenuSchema(**post_submenu)
        response = await submenu_services.create(session_storage["menu"]["id"], payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description'])
        session_storage['submenu'] = response.model_dump()

    async def test_list_empty_dishes(self, dish_services, session_storage):
        response = await dish_services.find_all(session_storage['submenu']['id'])
        assert response == []

    async def test_create_dish(self, dish_services, post_dish_1, session_storage):
        payload = DishSchema(**post_dish_1)
        response = await dish_services.create(session_storage['menu']['id'], session_storage['submenu']['id'], payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description', 'price'])
        session_storage['dish'] = response.model_dump()

    async def test_list_dishes_after_create(self, dish_services, session_storage):
        response = await dish_services.find_all(session_storage['submenu']['id'])
        assert response != []

    async def test_get_dish(self, dish_services, session_storage):
        response = await dish_services.find(session_storage['submenu']['id'], session_storage['dish']['id'])
        assert DishResponseSchema(**session_storage['dish']).compare_fields(response.model_dump(),
                                                                            fields=['title', 'description',
                                                                                    'price']) == True

    async def test_update_dish(self, dish_services, update_dish_1, session_storage):
        payload = DishUpdateSchema(**update_dish_1)
        response = await dish_services.update(session_storage['dish']['id'], payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description', 'price']) == True
        session_storage['dish'] = response.model_dump()

    async def test_get_dish_after_update(self, dish_services, session_storage):
        response = await dish_services.find(session_storage['submenu']['id'], session_storage['dish']['id'])
        assert DishResponseSchema(**session_storage['dish']).compare_fields(response.model_dump(),
                                                                                fields=['title', 'description',
                                                                                        'price']) == True

    async def test_delete_dish(self, dish_services, session_storage):
        response = await dish_services.delete(session_storage['dish']['id'])
        assert response == {
            "status": True,
            "message": "The dish has been deleted"
        }

        session_storage['dish']['id'] = '00000000-0000-0000-0000-000000000000'

    async def test_list_dishes_after_delete(self, dish_services, session_storage):
        response = await dish_services.find_all(session_storage['submenu']['id'])
        assert response == []

    async def test_get_dish_after_delete(self, dish_services, session_storage):
        try:
            response = await dish_services.find(session_storage['submenu']['id'], session_storage['dish']['id'])
            assert False
        except HTTPException as exc:
            assert exc.detail == 'dish not found'

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
