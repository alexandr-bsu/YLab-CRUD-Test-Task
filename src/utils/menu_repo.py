from utils.repository import SqlAlchemyRepository
from utils.menu_query_generator import generate_query_list_menu
from database import async_session

class MenuSqlAlchemyRepository(SqlAlchemyRepository):

    async def find_all(self, _filter=None):
        async with async_session() as session:
            stmt = generate_query_list_menu()

            if _filter is not None:
                stmt = stmt.filter(_filter)

            result = await session.execute(stmt)
            return result.mappings().all()

    async def update(self, id, data):
        await super().update(id, data)
        return await self.find(id)

