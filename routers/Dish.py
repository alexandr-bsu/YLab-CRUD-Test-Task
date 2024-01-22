from fastapi.routing import APIRouter
import database.queries.Dish as db
import schema.utils as schema_utils
from typing import List
from schema.Dish import DishSchema, DishUpdateSchema, DishResponseSchema
from uuid import UUID

router = APIRouter(prefix='/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', tags=['Dish'])


@router.post(path='/', status_code=201, response_model=DishResponseSchema)
async def create_dish(target_submenu_id, dish: DishSchema):
    dish_db = await db.create_dish(dish=dish, menu_id=target_submenu_id)
    return schema_utils.adapt_dish_orm_answer_to_schema(dish_db)


@router.get(path='/', status_code=200, response_model=List[DishResponseSchema])
async def list_dishes(target_menu_id: UUID, target_submenu_id: UUID):
    list_dish_db = await db.list_dish(target_submenu_id)
    return [schema_utils.adapt_dish_orm_answer_to_schema(dish) for dish in list_dish_db]

@router.get(path='/{dish_id}', status_code=200, response_model=DishResponseSchema)
async def get_dishes(target_menu_id: UUID, target_submenu_id: UUID, dish_id: UUID):
    dish_db = await db.get_dish(dish_id)
    return schema_utils.adapt_dish_orm_answer_to_schema(dish_db)

@router.patch(path='/{dish_id}', status_code=200, response_model=DishResponseSchema)
async def update_dish(target_menu_id: UUID, target_submenu_id: UUID, dish_id: UUID, dish: DishUpdateSchema):
    dish_db = await db.update_dish(dish_id, dish)
    return schema_utils.adapt_dish_orm_answer_to_schema(dish_db)


@router.delete('/{dish_id}', status_code=200)
async def delete_menu(target_menu_id: UUID, target_submenu_id: UUID, dish_id: UUID):
    await db.delete_dish(dish_id)
    return {
        "status": True,
        "message": "The dish has been deleted"
    }

