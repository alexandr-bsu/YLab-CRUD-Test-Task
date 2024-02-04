from repositories.abstract.AbstractCrud import AbstractCrud
from repositories.menu import MenuSqlRepository
from schemas.menu import MenuSchema, MenuUpdateSchema
from services.abstract.AbstractCrudService import AbstractCrudService
from .exceptions import raise_404


class MenuServices(AbstractCrudService):
    def __init__(self, menu_repository: AbstractCrud = MenuSqlRepository()):
        self.menu_repository: AbstractCrud = menu_repository

    async def create(self, data: MenuSchema):
        return await self.menu_repository.create(data, parent_id=None)

    @raise_404('menu not found')
    async def find(self, id):
        return await self.menu_repository.find(id)

    async def find_all(self):
        return await self.menu_repository.find_all(parent_id=None)

    @raise_404('menu not found')
    async def update(self, data: MenuUpdateSchema, id):
        await self.menu_repository.find(id)
        return await self.menu_repository.update(data, id)

    async def delete(self, id):
        await self.menu_repository.delete(id)
        return {
            "status": True,
            "message": "The menu has been deleted"
        }

    async def delete_all(self):
        await self.menu_repository.delete_all(parent_id=None)
        return {
            "status": True,
            "message": "All menu have been deleted"
        }
