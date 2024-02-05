from repositories.abstract.AbstractCrud import AbstractCrud

from repositories.repository import SqlAlchemyRepository
from sqlalchemy.orm import aliased
from sqlalchemy import select, func, distinct
from models.dish import Dish
from models.menu import Menu


def find_menu_query(**filter_by):
    submenu: Menu = aliased(Menu)
    query = (select(Menu.id,
                    Menu.title,
                    Menu.description,
                    func.count(distinct(submenu.id)).label('submenus_count'),
                    func.count(Dish.id).label('dishes_count'))
             .filter_by(**filter_by)
             .outerjoin(submenu, Menu.id == submenu.parent_id)
             .outerjoin(Dish, Dish.menu_id == submenu.id)
             .filter(Menu.parent_id.is_(None))
             .group_by(Menu.id))
    return query


class MenuSqlRepository(AbstractCrud):
    repo_engine: SqlAlchemyRepository = SqlAlchemyRepository(Menu)

    async def create(self, data, parent_id=None):
        return await self.repo_engine.create(data)

    async def find_all(self, parent_id=None):
        custom_query = find_menu_query()
        return await self.repo_engine.find_all(custom_query=custom_query)

    async def find(self, id):
        custom_query = find_menu_query(id=id)
        return await self.repo_engine.find(custom_query=custom_query)

    async def update(self, data, id):
        await self.repo_engine.update(data, id=id)
        return await self.find(id)

    async def delete(self, id):
        await self.repo_engine.delete(id=id)

    async def delete_all(self, parent_id=None):
        await self.repo_engine.delete()
