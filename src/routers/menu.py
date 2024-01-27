from fastapi.routing import APIRouter
from schemas.menu import MenuSchema, MenuResponseSchema, MenuUpdateSchema
from repositories.menu import MenuRepository
from services.menu import MenuServices
from typing import List
from uuid import UUID

router = APIRouter(prefix='/menus', tags=['menu'])


@router.post('/', status_code=201, response_model=MenuResponseSchema)
async def create_menu(data: MenuSchema):
    menu_services = MenuServices(MenuRepository())
    return await menu_services.create(data)

@router.get('/', response_model=List[MenuResponseSchema])
async def list_menu():
    menu_services = MenuServices(MenuRepository())
    return await menu_services.find_all()

@router.get('/{menu_id}', response_model=MenuResponseSchema)
async def get_menu(menu_id: UUID):
    menu_services = MenuServices(MenuRepository())
    return await menu_services.find(menu_id)

@router.patch('/{menu_id}', response_model=MenuResponseSchema)
async def update_menu(menu_id: UUID, data: MenuUpdateSchema):
    menu_services = MenuServices(MenuRepository())
    return await menu_services.update(menu_id, data)


@router.delete('/{menu_id}')
async def delete_menu(menu_id: UUID):
    menu_services = MenuServices(MenuRepository())
    return await menu_services.delete(menu_id)


