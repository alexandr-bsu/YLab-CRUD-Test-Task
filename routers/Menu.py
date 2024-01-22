from fastapi.routing import APIRouter
import database.queries.Menu as db
import schema.utils as schema_utils
from typing import List
from schema.Menu import MenuSchema, MenuUpdateSchema, MenuResponseSchema
from uuid import UUID

router = APIRouter(prefix='/menus')

@router.post(path='/', status_code=201, response_model=MenuResponseSchema)
async def create_menu(menu: MenuSchema):
    menu_db = await db.create_menu(menu=menu)
    return schema_utils.adapt_menu_orm_answer_to_schema(menu_db)


@router.get('/', status_code=200, response_model=List[MenuResponseSchema])
async def list_menu():
    list_menu_db = await db.list_menu()
    return [schema_utils.adapt_menu_orm_answer_to_schema(menu) for menu in list_menu_db]


@router.get('/{target_id}', status_code=200, response_model=MenuResponseSchema)
async def list_menu(target_id: UUID):
    menu_db = await db.get_menu(target_id)
    return schema_utils.adapt_menu_orm_answer_to_schema(menu_db)


@router.patch('/{target_id}', status_code=200, response_model=MenuResponseSchema)
async def update_menu(target_id: UUID, menu_data: MenuUpdateSchema):
    menu_db = await db.update_menu(target_id, menu_data)
    return schema_utils.adapt_menu_orm_answer_to_schema(menu_db)


@router.delete('/{target_id}', status_code=200)
async def delete_menu(target_id: UUID):
    await db.delete_menu(target_id)
    return {
        "status": True,
        "message": "The menu has been deleted"
    }
