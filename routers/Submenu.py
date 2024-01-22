from fastapi.routing import APIRouter
import database.queries.Menu as db
import schema.utils as schema_utils
from typing import List
from schema.Menu import MenuSchema, MenuUpdateSchema, SubmenuResponseSchema
from uuid import UUID

router = APIRouter(prefix='/menus/{target_menu_id}/submenus', tags=['Submenu'])


@router.post(path='/', status_code=201, response_model=SubmenuResponseSchema)
async def create_menu(target_menu_id: UUID, menu: MenuSchema):
    menu_db = await db.create_menu(menu=menu, is_root=False, parent_menu_id=target_menu_id)
    return schema_utils.adapt_menu_orm_answer_to_schema(menu_db)


@router.get('/', status_code=200, response_model=List[SubmenuResponseSchema])
async def list_menu(target_menu_id: UUID):
    list_menu_db = await db.list_submenu(target_menu_id)
    return [schema_utils.adapt_menu_orm_answer_to_schema(menu, is_root=False) for menu in list_menu_db]


@router.get('/{target_submenu_id}', status_code=200, response_model=SubmenuResponseSchema)
async def list_menu(target_menu_id: UUID, target_submenu_id: UUID):
    menu_db = await db.get_submenu(target_submenu_id, target_menu_id)
    return schema_utils.adapt_menu_orm_answer_to_schema(menu_db, is_root=False)


@router.patch('/{target_submenu_id}', status_code=200, response_model=SubmenuResponseSchema)
async def update_menu(target_submenu_id: UUID, menu_data: MenuUpdateSchema):
    menu_db = await db.update_menu(target_submenu_id, menu_data)
    return schema_utils.adapt_menu_orm_answer_to_schema(menu_db, is_root=False)


@router.delete('/{target_submenu_id}', status_code=200)
async def delete_menu(target_submenu_id: UUID):
    await db.delete_menu(target_submenu_id)
    return {
        "status": True,
        "message": "The submenu has been deleted"
    }
