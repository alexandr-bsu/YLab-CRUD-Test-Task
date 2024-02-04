from fastapi.routing import APIRouter
from schemas.menu import MenuSchema, SubmenuResponseSchema, MenuUpdateSchema
from cache.submenu_services import SubmenuServicesCache

from typing import List
from uuid import UUID

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['submenu'])


@router.post('/', status_code=201, response_model=SubmenuResponseSchema)
async def create_submenu(menu_id: UUID, data: MenuSchema):
    return await SubmenuServicesCache().create(data, menu_id)


@router.get('/', response_model=List[SubmenuResponseSchema])
async def list_submenu(menu_id: UUID):
    return await SubmenuServicesCache().find_all(menu_id)


@router.get('/{id}', response_model=SubmenuResponseSchema)
async def get_submenu(menu_id: UUID, id: UUID):
    return await SubmenuServicesCache().find(id, menu_id)


@router.patch('/{id}', response_model=SubmenuResponseSchema)
async def update_submenu(menu_id: UUID, id: UUID, data: MenuUpdateSchema):
    return await SubmenuServicesCache().update(data, id, menu_id)


@router.delete('/{id}')
async def delete_submenu(menu_id: UUID, id: UUID):
    return await SubmenuServicesCache().delete(id, menu_id)
