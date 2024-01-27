from utils.repository import AbstractRepository
from schemas.menu import MenuSchema, MenuUpdateSchema, MenuResponseSchema
from fastapi.exceptions import HTTPException


class MenuServices:
    def __init__(self, repo: AbstractRepository):
        self.menu_repo = repo

    async def create(self, data: MenuSchema):
        menu_dict = data.model_dump()
        menu = await self.menu_repo.create_one(menu_dict)
        return MenuResponseSchema(**menu)

    async def find_all(self):
        menus = await self.menu_repo.find_all()
        return [MenuResponseSchema(**row) for row in menus]

    async def find(self, menu_id):
        try:
            menu = await self.menu_repo.find(menu_id)
            return MenuResponseSchema(**menu)
        except IndexError:
            raise HTTPException(status_code=404, detail='menu not found')

    async def update(self, menu_id, data: MenuUpdateSchema):
        try:
            menu_dict = data.model_dump()
            menu = await self.menu_repo.update(menu_id, menu_dict)
            return MenuResponseSchema(**menu)
        except IndexError:
            raise HTTPException(status_code=404, detail='menu not found')

    async def delete(self, menu_id):
        await self.menu_repo.delete(menu_id)
        return {
                "status": True,
                "message": "The menu has been deleted"
            }
