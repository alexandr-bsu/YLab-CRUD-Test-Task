from repositories.submenu import SubmenuSqlRepository
from repositories.menu import MenuSqlRepository

from repositories.abstract.AbstractCrud import AbstractCrud as AbstractCrudRepo
from schemas.menu import MenuSchema, MenuUpdateSchema
from services.abstract.AbstractCrudService import AbstractCrudService
from .exceptions import raise_404, raise_400
from sqlalchemy.exc import NoResultFound
from fastapi.exceptions import HTTPException


class SubmenuServices(AbstractCrudService):
    def __init__(self, submenu_repository: AbstractCrudRepo = SubmenuSqlRepository(),
                 menu_repository: AbstractCrudRepo = MenuSqlRepository()):

        self.submenu_repository: AbstractCrudRepo = submenu_repository
        self.menu_repository: AbstractCrudRepo = menu_repository

    @raise_400('Cant create submenu in not existing menu')
    async def create(self, data: MenuSchema, parent_id):

        try:
            # Если подменю с parent_id не существует, то вызываем ислючение
            await self.submenu_repository.find(parent_id)
        except NoResultFound:
            return await self.submenu_repository.create(data, parent_id)

        # Если исключение NoResultFound не было вызвано, значит подменю c id = parent_id существует
        raise HTTPException(status_code=400, detail='Submenu cant be created in another submenu')

    @raise_404('submenu not found')
    async def find(self, id, parent_id):
        # Если меню с parent_id не существует то вызывается исключение HTTPException c кодом 404
        await self.menu_repository.find(parent_id)
        return await self.submenu_repository.find(id)

    async def find_all(self, parent_id):
        return await self.submenu_repository.find_all(parent_id)

    @raise_404('submenu not found')
    async def update(self, data: MenuUpdateSchema, id, parent_id):
        # Если меню с parent_id не существует то вызывается исключение HTTPException c кодом 404
        await self.menu_repository.find(parent_id)
        return await self.submenu_repository.update(data, id)

    async def delete(self, id):
        await self.submenu_repository.delete(id)
        return {
            'status': True,
            'message': 'The submenu has been deleted'
        }

    async def delete_all(self, parent_id):
        await self.submenu_repository.delete_all(parent_id)
        return {
            'status': True,
            'message': 'all submenus have been deleted'
        }
