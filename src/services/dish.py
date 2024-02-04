from repositories.abstract.AbstractCrud import AbstractCrud
from repositories.menu import MenuSqlRepository
from repositories.submenu import SubmenuSqlRepository
from repositories.dish import DishSqlRepository
from schemas.dish import DishSchema, DishUpdateSchema
from services.abstract.AbstractCrudService import AbstractCrudService
from sqlalchemy.exc import NoResultFound
from fastapi.exceptions import HTTPException
from .exceptions import raise_404

class DishServices(AbstractCrudService):
    def __init__(self,
                 dish_repository: AbstractCrud = DishSqlRepository(),
                 submenu_repository: AbstractCrud = SubmenuSqlRepository(),
                 menu_repository: AbstractCrud = MenuSqlRepository()):

        self.dish_repository: AbstractCrud = dish_repository
        self.submenu_repository: AbstractCrud = submenu_repository
        self.menu_repository: AbstractCrud = menu_repository

    async def create(self, data: DishSchema, submenu_id, main_menu_id):
        try:
            # Если меню с main_menu_id не существует, то вызываем исключение
            await self.menu_repository.find(main_menu_id)
            # Если подменю с submenu_id не существует, то вызываем ислючение
            await self.submenu_repository.find(submenu_id)

        except NoResultFound:
            raise HTTPException(
                                status_code=400,
                                detail='It\'s impossible to create dish. Check menu\'s id or submenu\'s id'
                                )

        result = await self.dish_repository.create(data, submenu_id)

        return result

    @raise_404('dish not found')
    async def find(self, id, submenu_id, main_menu_id):
        # Если меню с main_menu_id не существует то вызывается исключение HTTPException c кодом 404
        await self.menu_repository.find(main_menu_id)
        # Если меню с submenu_id не существует то вызывается исключение HTTPException c кодом 404
        await self.submenu_repository.find(submenu_id)

        return await self.dish_repository.find(id)

    async def find_all(self, submenu_id):
        return await self.dish_repository.find_all(submenu_id)

    @raise_404('dish not found')
    async def update(self, data: DishUpdateSchema, id, submenu_id, main_menu_id):
        # Если меню с main_menu_id не существует то вызывается исключение HTTPException c кодом 404
        await self.menu_repository.find(main_menu_id)
        # Если меню с submenu_id не существует то вызывается исключение HTTPException c кодом 404
        await self.submenu_repository.find(submenu_id)

        return await self.dish_repository.update(data, id)

    async def delete(self, id):
        await self.dish_repository.delete(id)
        return {
            'status': True,
            'message': 'The dish has been deleted'
        }

    async def delete_all(self, submenu_id):
        await self.dish_repository.delete_all(submenu_id)
        return {
            'status': True,
            'message': 'All dishes have been deleted'
        }
