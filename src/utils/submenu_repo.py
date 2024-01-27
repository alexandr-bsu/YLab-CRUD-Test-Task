from utils.repository import SqlAlchemyRepository
from utils.menu_query_generator import generate_query_list_submenu
from database import async_session


class SubmenuSqlAlchemyRepository(SqlAlchemyRepository):

    async def find_all(self, parent_id, _filter=None):
        async with async_session() as session:
            stmt = generate_query_list_submenu(parent_id)

            if _filter is not None:
                stmt = stmt.filter(_filter)

            result = await session.execute(stmt)
            return result.mappings().all()

    async def find(self, parent_id, id):
        return (await self.find_all(parent_id, self.model.id == id))[0]

    async def update(self, parent_id, id, data):
        await super().update(id, data)
        return await self.find(parent_id, id)
