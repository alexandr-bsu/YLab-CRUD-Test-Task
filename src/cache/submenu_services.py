from services.abstract.AbstractCrudService import AbstractCrudService
from services.submenu import SubmenuServices
import pickle

from database import redis_client


class SubmenuServicesCache(AbstractCrudService):
    def __init__(self, submenu_services: AbstractCrudService = SubmenuServices()):
        self.submenu_services = submenu_services

    async def create(self, data, menu_id):
        submenu = await self.submenu_services.create(data, menu_id)
        # Invalid menu's cache, cause of new submenu was added
        await redis_client.delete(f'menu_menu_id:{menu_id}')
        await redis_client.delete(f'submenu_menu_id:{menu_id}')
        return submenu

    async def find_all(self, menu_id):
        submenu_list = await redis_client.get(f'submenu_menu_id:{menu_id}')
        if submenu_list is None:
            result = await self.submenu_services.find_all(menu_id)
            await redis_client.set(f'submenu_menu_id:{menu_id}', pickle.dumps(result))
            return result
        else:
            return pickle.loads(submenu_list)

    async def find(self, id, menu_id):
        submenu = await redis_client.get(f'submenu_menu_id:{menu_id}_submenu_id:{id}')
        if submenu is None:
            result = await self.submenu_services.find(id, menu_id)
            await redis_client.set(f'submenu_menu_id:{menu_id}_submenu_id:{id}', pickle.dumps(result))
            return result
        return pickle.loads(submenu)

    async def update(self, data, id, menu_id):
        result = await self.submenu_services.update(data, id, menu_id)
        await redis_client.set(f'submenu_menu_id:{menu_id}_submenu_id:{id}', pickle.dumps(result))
        return result

    async def delete(self, id, menu_id):
        # TODO: Add menu_list cache invalidating
        await redis_client.delete(f'menu_list')
        await redis_client.delete(f'menu_menu_id:{menu_id}')
        await redis_client.delete(f'submenu_menu_id:{menu_id}_submenu_id:{id}')
        await redis_client.delete(f'dish_menu_id:{menu_id}_submenu_id:{id}_*')

        return await self.submenu_services.delete(id)

    async def delete_all(self, menu_id):
        await redis_client.delete(f'menu_id:{menu_id}')
        await redis_client.delete(f'submenu_menu_id:{menu_id}_*')
        await redis_client.delete(f'dish_menu_id:{menu_id}_*')

        return await self.submenu_services.delete_all(menu_id)
