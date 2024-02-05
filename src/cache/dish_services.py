from services.abstract.AbstractCrudService import AbstractCrudService
from services.dish import DishServices
import pickle

from database import redis_client


class DishServicesCache(AbstractCrudService):
    def __init__(self, dish_services: AbstractCrudService = DishServices()):
        self.dish_services = dish_services

    async def create(self, data, submenu_id, menu_id):
        dish = await self.dish_services.create(data, submenu_id, menu_id)
        await redis_client.delete(f'menu_menu_id:{menu_id}')
        await redis_client.delete(f'submenu_menu_id:{menu_id}_submenu_id:{submenu_id}')
        await redis_client.delete(f'dish_menu_id:{menu_id}_submenu_id:{submenu_id}_dish_id{dish.id}')
        return dish

    async def find_all(self, submenu_id, menu_id):
        dish_list = await redis_client.get(f'dish_menu_id:{menu_id}_submenu_id:{submenu_id}')
        if dish_list is None:
            result = await self.dish_services.find_all(submenu_id)

            await redis_client.set(f'dish_menu_id:{menu_id}_submenu_id:{submenu_id}', pickle.dumps(result))
            return result
        else:
            return pickle.loads(dish_list)

    async def find(self, id, submenu_id, menu_id):
        dish = await redis_client.get(f'dish_menu_id:{menu_id}_submenu_id:{submenu_id}_dish_id:{id}')
        if dish is None:
            result = await self.dish_services.find(id, submenu_id, menu_id)
            await redis_client.set(f'dish_menu_id:{menu_id}_submenu_id:{submenu_id}_dish_id:{id}', pickle.dumps(result))
            return result
        return pickle.loads(dish)

    async def update(self, data, id, submenu_id, menu_id):
        result = await self.dish_services.update(data, id, submenu_id, menu_id)
        await redis_client.set(f'dish_menu_id:{menu_id}_submenu_id:{submenu_id}_dish_id:{id}', pickle.dumps(result))
        return result

    async def delete(self, id, submenu_id, menu_id):
        await redis_client.delete(f'menu_id:{menu_id}')
        await redis_client.delete(f'submenu_menu_id:{menu_id}_submenu_id:{submenu_id}')
        await redis_client.delete(f'dish_menu_id:{menu_id}_submenu_id:{submenu_id}_dish_id:{id}')
        return await self.dish_services.delete(id)

    async def delete_all(self, menu_id):
        await redis_client.delete(f'menu_id:{menu_id}')
        await redis_client.delete(f'submenu_menu_id:{menu_id}_*')
        await redis_client.delete(f'dish_menu_id:{menu_id}_*')
        return await self.dish_services.delete_all(menu_id)