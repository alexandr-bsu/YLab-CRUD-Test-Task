from fastapi.routing import APIRouter
from schemas.dish import DishSchema, DishResponseSchema, DishUpdateSchema
from repositories.dish import DishRepository
from services.dish import DishServices
from typing import List
from uuid import UUID

router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['dish'])


@router.post('/', status_code=201, response_model=DishResponseSchema)
async def create_dish(menu_id: UUID, submenu_id: UUID, data: DishSchema):
    dish_services = DishServices(DishRepository())
    return await dish_services.create(menu_id, submenu_id, data)


@router.get('/', response_model=List[DishResponseSchema])
async def list_dish(menu_id: UUID, submenu_id: UUID):
    dish_services = DishServices(DishRepository())
    return await dish_services.find_all(submenu_id)

@router.get('/{dish_id}', response_model=DishResponseSchema)
async def get_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    dish_services = DishServices(DishRepository())
    return await dish_services.find(submenu_id, dish_id)


@router.patch('/{dish_id}', response_model=DishResponseSchema)
async def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, data: DishUpdateSchema):
    dish_services = DishServices(DishRepository())
    return await dish_services.update(dish_id, data)


@router.delete('/{dish_id}')
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    dish_services = DishServices(DishRepository())
    return await dish_services.delete(dish_id)
