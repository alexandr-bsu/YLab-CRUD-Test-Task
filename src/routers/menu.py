from fastapi.routing import APIRouter
from schemas.menu import MenuSchema, MenuResponseSchema, MenuUpdateSchema
from services.menu import MenuServices
from typing import List
from uuid import UUID

router = APIRouter(prefix='/menus', tags=['menu'])


@router.post('/', status_code=201, response_model=MenuResponseSchema)
async def create_menu(data: MenuSchema):
    return await MenuServices().create(data)

@router.get('/', response_model=List[MenuResponseSchema])
async def list_menu():
    return await MenuServices().find_all()

@router.get('/{id}', response_model=MenuResponseSchema)
async def get_menu(id: UUID):
    return await MenuServices().find(id)

@router.patch('/{id}', response_model=MenuResponseSchema)
async def update_menu(id: UUID, data: MenuUpdateSchema):
    return await MenuServices().update(data, id)

@router.delete('/{id}')
async def delete_menu(id: UUID):
    return await MenuServices().delete(id)


