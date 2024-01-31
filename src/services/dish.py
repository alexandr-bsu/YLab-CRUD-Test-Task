from utils.repository import AbstractRepository
from schemas.dish import *
from fastapi.exceptions import HTTPException
from repositories.submenu import SubmenuRepository
from sqlalchemy.exc import NoResultFound



class DishServices:
    def __init__(self, repo: AbstractRepository):
        self.dish_repo = repo
        self.submenu_repo = SubmenuRepository()

    async def create(self, menu_id, submenu_id, data: DishSchema):
        try:
            await self.submenu_repo.find(menu_id, submenu_id)
        except IndexError:
            raise HTTPException(status_code=404, detail='dish can be added to submenu only')

        dish_dict = data.model_dump()
        dish_dict['menu_id'] = submenu_id
        dish = await self.dish_repo.create_one(dish_dict)
        return DishResponseSchema(**dish)

    async def find_all(self, submenu_id):
        dishes = await self.dish_repo.find_all(submenu_id)
        return [DishResponseSchema(**row) for row in dishes]

    async def find(self, submenu_id, dish_id):
        try:
            dish = await self.dish_repo.find(submenu_id, dish_id)
            return DishResponseSchema(**dish)
        except IndexError:
            raise HTTPException(status_code=404, detail='dish not found')

    async def update(self, dish_id, data: DishUpdateSchema):
        try:
            dish_dict = data.model_dump()
            dish = await self.dish_repo.update(dish_id, dish_dict)
            return DishResponseSchema(**dish)
        except NoResultFound:
            raise HTTPException(status_code=404, detail='dish not found')

    async def delete(self, dish_id):
        await self.dish_repo.delete(dish_id)
        return {
                "status": True,
                "message": "The dish has been deleted"
            }


    async def delete_all(self):
        self.dish_repo.delete_all()
        return {
            "status": True,
            "message": "All dishes have been deleted"
        }
