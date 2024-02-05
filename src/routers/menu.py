from fastapi.routing import APIRouter
from schemas.menu import MenuSchema, MenuResponseSchema, MenuUpdateSchema
from cache.menu_services import MenuServicesCache
from typing import List
from uuid import UUID

router = APIRouter(prefix='/menus', tags=['menu'])


@router.post('/', status_code=201, response_model=MenuResponseSchema)
async def create_menu(data: MenuSchema):
    return await MenuServicesCache().create(data)


@router.get('/', response_model=List[MenuResponseSchema])
async def list_menu():
    return await MenuServicesCache().find_all()


@router.get('/{id}', response_model=MenuResponseSchema)
async def get_menu(id: UUID):
    return await MenuServicesCache().find(id)


@router.patch('/{id}', response_model=MenuResponseSchema)
async def update_menu(id: UUID, data: MenuUpdateSchema):
    return await MenuServicesCache().update(data, id)


@router.delete('/{id}')
async def delete_menu(id: UUID):
    return await MenuServicesCache().delete(id)
