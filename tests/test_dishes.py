from src.schemas.dish import DishSchema, DishUpdateSchema, DishResponseSchema
from src.schemas.menu import MenuSchema
from httpx import AsyncClient
from main import app
import pytest
from uuid import UUID
from fastapi.exceptions import HTTPException


@pytest.mark.usefixtures('init_db_fixture')
class TestDish:

    async def test_list_empty_dishes(self, post_menu, post_submenu, menu_services, submenu_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()
            menu_db = await menu_services.create(MenuSchema(**post_menu))
            submenu_db = await submenu_services.create(menu_db.id, MenuSchema(**post_menu))

            response = await ac.get(f'/menus/{menu_db.id}/submenus/{submenu_db.id}/dishes/')

            assert response.status_code == 200
            assert response.json() == []
            await menu_services.delete_all()

    async def test_create_dish(self, post_submenu, post_menu, menu_services, post_dish_1, submenu_services, dish_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()
            menu_db = await menu_services.create(MenuSchema(**post_menu))
            submenu_db = await submenu_services.create(menu_db.id, MenuSchema(**post_submenu))

            payload = DishSchema(**post_dish_1, menu_id=submenu_db.id)
            response = await ac.post(f'/menus/{menu_db.id}/submenus/{submenu_db.id}/dishes/',
                                     json=payload.model_dump())

            dish_id = response.json()['id']
            dish_db = await dish_services.find(submenu_db.id, dish_id)

            assert response.status_code == 201, "incorrect response status code. waiting 201"
            assert dish_db.id is not None, "dish's id is absent in DB"
            assert dish_db.id == UUID(dish_id), "unexpected dish's id in DB"
            assert dish_db.title is not None, "dish's title is absent in DB"
            assert dish_db.title == response.json()['title'], "unexpected dish's title in DB"
            assert dish_db.title == post_dish_1['title'], "dish's title in request data mutated"
            assert dish_db.description is not None, "dish's description is absent in DB"
            assert dish_db.description == response.json()['description'], "unexpected dish's description in DB"
            assert dish_db.description == post_dish_1['description'], "submenu's dish description in request data mutated"
            assert dish_db.price is not None, "dish's price is absent in DB"
            assert dish_db.price == response.json()['price'], "unexpected dish's price in DB"
            assert dish_db.price == post_dish_1['price'], "submenu's dish price in request data mutated"

            try:
                await dish_services.create('00000000-0000-0000-0000-000000000000','00000000-0000-0000-0000-000000000000', DishSchema(**post_dish_1))
                assert False
            except HTTPException as exc:
                assert exc.status_code == 400
                assert exc.detail == "dish can be added to submenu only"

            try:
                await dish_services.create(menu_db.id, menu_db.id, DishSchema(**post_dish_1))
                assert False
            except HTTPException as exc:
                assert exc.status_code == 400
                assert exc.detail == "dish can be added to submenu only"

            await menu_services.delete_all()

    async def test_list_dishes(self, post_menu, post_submenu, menu_services, post_dish_1, submenu_services, dish_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu = await menu_services.create(MenuSchema(**post_menu))
            submenu = await submenu_services.create(menu.id, MenuSchema(**post_submenu))
            dish = await dish_services.create(menu.id, submenu.id, DishSchema(**post_dish_1))

            response = await ac.get(f"/menus/{menu.id}/submenus/")

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert response.json() != [], "List of dishes is not displayed"

            await menu_services.delete_all()

    async def test_get_dish(self, post_menu, post_submenu, post_dish_1, update_dish_1, menu_services, submenu_services, dish_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu_db = await menu_services.create(MenuSchema(**post_menu))
            submenu_db = await submenu_services.create(menu_db.id, MenuSchema(**post_submenu))
            dish_db = await dish_services.create(menu_db.id, submenu_db.id, DishSchema(**post_dish_1))

            response = await ac.get(f"/menus/{menu_db.id}/submenus/{submenu_db.id}/dishes/{dish_db.id}")

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert response.json()['id'] is not None, "dish's id is absent in get response"
            assert dish_db.id == UUID(response.json()['id']), "unexpected dish's id in get response"
            assert response.json()['title'] is not None, "dish's title is absent in get response"
            assert dish_db.title == response.json()['title'], "unexpected dish's id in get response"
            assert response.json()['title'] == post_dish_1['title'], "dish's title in response data is mutated"

            assert response.json()['description'] is not None, "dish's description is absent in get response"
            assert dish_db.description == response.json()['description'], "unexpected dish's id in get response"
            assert response.json()['description'] == post_dish_1['description'], "dish's description in response data is mutated"

            assert response.json()['price'] is not None, "dish's price is absent in get response"
            assert dish_db.price == response.json()['price'], "unexpected dish's price in get response"
            assert response.json()['price'] == post_dish_1['price'], "dish's price in response data is mutated"

            response_get_not_existing_submenu = await ac.get(f"/menus/3c6b8785-c06f-43b5-b700-1ff5436db9a8/submenus/439d26f9-f4bc-47d1-99de-f2b82f175a68/dishes/3c6b8785-c06f-43b5-b700-1ff5436db9a8")
            assert response_get_not_existing_submenu.status_code == 404, "incorrect response status code. waiting 404"
            assert response_get_not_existing_submenu.json() == {
                'detail': 'dish not found'}, "incorrect response detail. waiting: dish not found"

            await menu_services.delete_all()


    async def test_update_dish(self, post_menu, post_submenu, post_dish_1, update_dish_1, menu_services, submenu_services, dish_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu_db = await menu_services.create(MenuSchema(**post_menu))
            submenu_db = submenu_db = await submenu_services.create(menu_db.id, MenuSchema(**post_submenu))
            dish_db = await dish_services.create(menu_db.id, submenu_db.id, DishSchema(**post_dish_1))

            payload = DishSchema(**update_dish_1)

            response = await ac.patch(f"/menus/{menu_db.id}/submenus/{submenu_db.id}/dishes/{dish_db.id}", json=payload.model_dump())
            update_dish_db = await dish_services.find(submenu_db.id, dish_db.id)

            assert response.status_code == 200, "incorrect response status code. waiting 200"
            assert update_dish_db.id is not None, "dish's id is absent in DB"
            assert update_dish_db.id == dish_db.id, "dish's id in DB is changed"

            assert update_dish_db.title is not None, "dish's title is absent in DB"
            assert update_dish_db.title == response.json()['title'], "unexpected dish's title in DB"
            assert update_dish_db.title == update_dish_1['title'], "dish's title in DB hasn't changed"

            assert update_dish_db.description is not None, "dish's description is absent in DB"
            assert update_dish_db.description == response.json()['description'], "unexpected dish's description in DB"
            assert update_dish_db.description == update_dish_1['description'], "dish's description in DB hasn't changed"

            assert update_dish_db.price is not None, "dish's price is absent in DB"
            assert update_dish_db.price == response.json()['price'], "unexpected dish's price in DB"
            assert update_dish_db.price == update_dish_1['price'], "dish's price in DB hasn't changed"

            response_update_not_existing_dish = await ac.patch(f"/menus/{menu_db.id}/submenus/00000000-0000-0000-0000-000000000000/dishes/00000000-0000-0000-0000-000000000000",
                                                               json=payload.model_dump())

            assert response_update_not_existing_dish.status_code == 404, "incorrect response status code. waiting 404"
            assert response_update_not_existing_dish.json() == {
                'detail': 'dish not found'}, "incorrect response detail. waiting: dish not found"

        await menu_services.delete_all()

    async def test_delete_dishes(self, post_menu, post_submenu, post_dish_1, update_dish_1, menu_services, submenu_services, dish_services):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            await menu_services.delete_all()

            menu_db = await menu_services.create(MenuSchema(**post_menu))
            submenu_db = submenu_db = await submenu_services.create(menu_db.id, MenuSchema(**post_submenu))
            dish_db = await dish_services.create(menu_db.id, submenu_db.id, DishSchema(**post_dish_1))

            response = await ac.delete(f"/menus/{menu_db.id}/submenus/{submenu_db.id}/dishes/{dish_db.id}")

            assert response.status_code == 200
            assert response.json() == {
                "status": True,
                "message": "The dish has been deleted"
            }

            try:
                deleted_dish_result_db = await dish_services.find(submenu_db.id, dish_db.id)
                assert False
            except HTTPException as exc:
                assert exc.status_code == 404, "incorrect response status code. waiting 404"
                assert exc.detail == "dish not found", "incorrect response detail. waiting: dish not found"

        await menu_services.delete_all()



