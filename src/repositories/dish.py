from abc import ABC
from repositories.abstract.AbstractCrud import AbstractCrud

from repositories.repository import SqlAlchemyRepository
from models.dish import Dish


class DishSqlRepository(AbstractCrud, ABC):
    repo_engine: SqlAlchemyRepository = SqlAlchemyRepository(Dish)

    async def create(self, data, menu_id):
        return await self.repo_engine.create(data, menu_id=menu_id)

    async def find_all(self, menu_id):
        return await self.repo_engine.find_all(menu_id=menu_id)

    async def find(self, id):
        return await self.repo_engine.find(id=id)

    async def update(self, data, id):
        await self.repo_engine.update(data, id=id)
        return await self.repo_engine.find(id=id)

    async def delete(self, id):
        return await self.repo_engine.delete(id=id)

    async def delete_all(self, menu_id):
        return await self.repo_engine.delete(menu_id=menu_id)


