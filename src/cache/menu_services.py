from services.abstract.AbstractCrudService import AbstractCrudService
from services.menu import MenuServices
import pickle
from database import redis_client


class MenuServicesCache(AbstractCrudService):
    def __init__(self, menu_services: AbstractCrudService = MenuServices()):
        self.menu_services = menu_services

    async def create(self, data):
        menu = await self.menu_services.create(data)
        await redis_client.delete(f'menu_list')
        return menu

    async def find_all(self):
        menu_list = await redis_client.get('menu_list')
        if menu_list is None:
            result = await self.menu_services.find_all()
            await redis_client.set('menu_list', pickle.dumps(result))
            return result
        else:
            return pickle.loads(menu_list)

    async def find(self, id):
        print('menu find')

        menu = await redis_client.get(f'menu_menu_id:{id}')
        if menu is None:
            result = await self.menu_services.find(id)
            await redis_client.set(f'menu_menu_id:{id}', pickle.dumps(result))
            return result
        return pickle.loads(menu)

    async def update(self, data, id):
        result = await self.menu_services.update(data, id)
        await redis_client.set(f'menu_menu_id:{id}', pickle.dumps(result))
        return result

    async def delete(self, id):
        await redis_client.delete(f'menu_menu_id:{id}')
        await redis_client.delete(f'submenu_menu_id:{id}_*')
        await redis_client.delete(f'dish_menu_id:{id}_*')

        return await self.menu_services.delete(id)

    async def delete_all(self):
        await redis_client.delete('*')
        return await self.menu_services.delete_all()
