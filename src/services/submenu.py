from utils.repository import AbstractRepository
from repositories.menu import MenuRepository
from services.menu import MenuServices
from schemas.menu import MenuSchema, MenuUpdateSchema, SubmenuResponseSchema
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound


class SubmenuServices:
    def __init__(self, repo: AbstractRepository):
        self.submenu_repo = repo

    async def create(self, menu_id, data: MenuSchema):
        menu_dict = data.model_dump()
        menu_dict['parent_id'] = menu_id

        try:
            await MenuServices(MenuRepository()).find(menu_id)
        except HTTPException:
            raise HTTPException(detail="Cant create submenu in not existing menu", status_code=400)


        try:
            menu = await self.submenu_repo.create_one(menu_dict)
            return SubmenuResponseSchema(**menu)
        except IntegrityError:
            raise HTTPException(detail="Cant create submenu in not existing menu", status_code=400)

    async def find_all(self, menu_id):
        menus = await self.submenu_repo.find_all(parent_id=menu_id)
        return [SubmenuResponseSchema(**row) for row in menus]

    async def find(self, menu_id, submenu_id):
        try:
            menu = await self.submenu_repo.find(menu_id, submenu_id)
            return SubmenuResponseSchema(**menu)
        except IndexError:
            raise HTTPException(status_code=404, detail='submenu not found')

    async def update(self, menu_id, submenu_id, data: MenuUpdateSchema):
        try:
            menu_dict = data.model_dump()
            menu = await self.submenu_repo.update(menu_id, submenu_id, menu_dict)
            return SubmenuResponseSchema(**menu)
        except NoResultFound:
            raise HTTPException(status_code=404, detail='submenu not found')

    async def delete(self, submenu_id):
        await self.submenu_repo.delete(submenu_id)
        return {
            "status": True,
            "message": "The submenu has been deleted"
        }

    async def delete_all(self):
        self.submenu_repo.delete_all()
        return {
            "status": True,
            "message": "All submenus have been deleted"
        }
