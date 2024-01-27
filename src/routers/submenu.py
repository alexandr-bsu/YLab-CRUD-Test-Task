from fastapi.routing import APIRouter
from schemas.menu import MenuSchema, SubmenuResponseSchema, MenuUpdateSchema
from repositories.submenu import SubmenuRepository
from services.submenu import SubmenuServices

from typing import List
from uuid import UUID

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['submenu'])


@router.post('/', status_code=201, response_model=SubmenuResponseSchema)
async def create_submenu(menu_id: UUID,  data: MenuSchema):
    submenu_services = SubmenuServices(SubmenuRepository())
    return await submenu_services.create(menu_id, data)

@router.get('/', response_model=List[SubmenuResponseSchema])
async def list_submenu(menu_id: UUID):
    submenu_services = SubmenuServices(SubmenuRepository())
    return await submenu_services.find_all(menu_id)

@router.get('/{submenu_id}', response_model=SubmenuResponseSchema)
async def get_submenu(menu_id: UUID, submenu_id: UUID):
    submenu_services = SubmenuServices(SubmenuRepository())
    return await submenu_services.find(menu_id, submenu_id)

@router.patch('/{submenu_id}', response_model=SubmenuResponseSchema)
async def update_submenu(menu_id: UUID, submenu_id: UUID, data: MenuUpdateSchema):
    submenu_services = SubmenuServices(SubmenuRepository())
    return await submenu_services.update(menu_id, submenu_id, data)

@router.delete('/{submenu_id}')
async def delete_submenu(menu_id: UUID, submenu_id: UUID):
    submenu_services = SubmenuServices(SubmenuRepository())
    return await submenu_services.delete(submenu_id)
