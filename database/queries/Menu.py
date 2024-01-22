from ..engine import async_session
from sqlalchemy import delete, update, insert, literal_column
from ..models.Menu import Menu
from ..utils import generate_query_list_menu, generate_query_list_submenu
from schema.Menu import MenuSchema, MenuUpdateSchema
from sqlalchemy.exc import NoResultFound
from fastapi.exceptions import HTTPException
async def create_menu(menu: MenuSchema, is_root=True, parent_menu_id=None):
    async with async_session() as session:
        query = insert(Menu) \
            .values(**menu.model_dump(), is_root=is_root, parent_menu_id=parent_menu_id) \
            .returning(Menu.id, Menu.title, Menu.description, literal_column('0'), literal_column('0'))

        menu_db = await session.execute(query)
        await session.commit()
        return menu_db.one()


async def list_menu():
    async with async_session() as session:
        query = generate_query_list_menu()
        result = await session.execute(query)
        return result.all()


async def get_menu(id):
    async with async_session() as session:
        query = generate_query_list_menu().filter(Menu.id == id)
        try:
            result = await session.execute(query)
            return result.one()
        except NoResultFound as ex:
            raise HTTPException(status_code=404, detail="menu not found")


async def list_submenu(parent_menu_id):
    async with async_session() as session:
        try:
            await session.get(Menu, parent_menu_id)
        except NoResultFound as ex:
            raise HTTPException(status_code=404, detail="menu not found")

        query = generate_query_list_submenu(parent_menu_id)
        result = await session.execute(query)
        return result.all()


async def get_submenu(submenu_id, menu_id):
    async with async_session() as session:
        try:
            await session.get(Menu, submenu_id)
            await session.get(Menu, menu_id)

            query = generate_query_list_submenu(menu_id).filter(Menu.id == submenu_id)
            result = await session.execute(query)
            return result.one()

        except NoResultFound:
            raise HTTPException(status_code=404, detail='submenu not found')

async def update_menu(id, menu_data: MenuUpdateSchema):
    async with async_session() as session:
        try:
            session.get(Menu, id)
        except NoResultFound as ex:
            raise HTTPException(status_code=404, detail="menu not found")

        query = update(Menu) \
            .values(**menu_data.model_dump(exclude_unset=True)) \
            .filter_by(id=id)

        await session.execute(query)
        await session.commit()

        return await get_menu(id)


async def delete_menu(id):
    async with async_session() as session:
        query = delete(Menu).filter_by(id=id)
        await session.execute(query)
        await session.commit()
