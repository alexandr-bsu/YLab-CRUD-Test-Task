from abc import ABC
from repositories.abstract.AbstractCrud import AbstractCrud
from repositories.repository import SqlAlchemyRepository
from sqlalchemy import select, func
from models.dish import Dish
from models.menu import Menu


def find_submenu_query(**filter_by):
    query = (
        select(Menu.id,
               Menu.title,
               Menu.description,
               func.count(Dish.id).label('dishes_count'))
        .filter_by(**filter_by)
        .filter(Menu.parent_id.is_not(None))
        .outerjoin(Dish, Dish.menu_id == Menu.id)
        .group_by(Menu.id)
    )
    return query


def find_all_submenu_query(parent_id, **filter_by):
    query = find_submenu_query(**filter_by).filter(Menu.parent_id == parent_id)
    return query


class SubmenuSqlRepository(AbstractCrud, ABC):
    repo_engine: SqlAlchemyRepository = SqlAlchemyRepository(Menu)

    async def create(self, data, parent_id):
        return await self.repo_engine.create(data, parent_id=parent_id)

    async def find_all(self, parent_id):
        custom_query = find_all_submenu_query(parent_id=parent_id)
        return await self.repo_engine.find_all(custom_query=custom_query)

    async def find(self, id):
        custom_query = find_submenu_query(id=id)
        return await self.repo_engine.find(custom_query=custom_query)

    async def update(self, data, id):
        await self.repo_engine.update(data, id=id)
        return await self.find(id)

    async def delete(self, id):
        await self.repo_engine.delete(id=id)

    async def delete_all(self, parent_id):
        await self.repo_engine.delete(parent_id=parent_id)
