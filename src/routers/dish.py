from fastapi.routing import APIRouter
from schemas.dish import DishSchema, DishResponseSchema, DishUpdateSchema
from cache.dish_services import DishServicesCache
from typing import List
from uuid import UUID

router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['dish'])


@router.post('/', status_code=201, response_model=DishResponseSchema)
async def create_dish(menu_id: UUID, submenu_id: UUID, data: DishSchema):
    return await DishServicesCache().create(data, submenu_id, menu_id)


@router.get('/', response_model=List[DishResponseSchema])
async def list_dish(menu_id: UUID, submenu_id: UUID):
    return await DishServicesCache().find_all(submenu_id, menu_id)


@router.get('/{dish_id}', response_model=DishResponseSchema)
async def get_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    return await DishServicesCache().find(dish_id, submenu_id, menu_id)


@router.patch('/{dish_id}', response_model=DishResponseSchema)
async def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, data: DishUpdateSchema):
    return await DishServicesCache().update(data, dish_id, submenu_id, menu_id)


@router.delete('/{dish_id}')
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    return await DishServicesCache().delete(dish_id, submenu_id, menu_id)
