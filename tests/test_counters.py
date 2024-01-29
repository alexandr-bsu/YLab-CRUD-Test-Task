from src.schemas.menu import MenuSchema, MenuResponseSchema, SubmenuResponseSchema
from src.schemas.dish import DishSchema
import pytest


@pytest.mark.usefixtures('init_db_fixture')
class TestCounters:
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

    async def test_create_dish_1(self, dish_services, post_dish_1, session_storage):
        payload = DishSchema(**post_dish_1)
        response = await dish_services.create(session_storage['menu']['id'], session_storage['submenu']['id'], payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description', 'price'])
        session_storage['dish_1'] = response.model_dump()

    async def test_create_dish_2(self, dish_services, post_dish_2, session_storage):
        payload = DishSchema(**post_dish_2)
        response = await dish_services.create(session_storage['menu']['id'], session_storage['submenu']['id'], payload)
        assert payload.compare_fields(response.model_dump(), ['title', 'description', 'price'])
        session_storage['dish_2'] = response.model_dump()

    async def test_menu_counters(self, menu_services, session_storage):
        response = await menu_services.find(session_storage['menu']['id'])
        assert response.model_dump()['dishes_count'] == 2
        assert response.model_dump()['submenus_count'] == 1
        assert MenuResponseSchema(**session_storage['menu']).compare_fields(response.model_dump(),
                                                                            fields=['title', 'description']) == True

    async def test_submenu_counters(self, submenu_services, session_storage):
        response = await submenu_services.find(session_storage['menu']['id'], session_storage['submenu']['id'])
        assert response.model_dump()['dishes_count'] == 2
        assert SubmenuResponseSchema(**session_storage['submenu']).compare_fields(response.model_dump(),
                                                                                  fields=['title',
                                                                                          'description']) == True

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

    async def test_list_dishes_after_delete_submenu(self, dish_services, session_storage):
        response = await dish_services.find_all(session_storage['submenu']['id'])
        assert response == []

    async def test_menu_counters_after_delete_submenu(self,menu_services, session_storage):
        response = await menu_services.find(session_storage['menu']['id'])
        assert response.model_dump()['dishes_count'] == 0
        assert response.model_dump()['submenus_count'] == 0
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

