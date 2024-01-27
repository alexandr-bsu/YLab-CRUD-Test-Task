from utils.repository import SqlAlchemyRepository
from database import async_session
from sqlalchemy import select
class DishSqlAlchemyRepository(SqlAlchemyRepository):

    async def find_all(self, menu_id, _filter=None):
        async with async_session() as session:
            stmt = select(self.model.id, self.model.title, self.model.description, self.model.price)\
                .filter(self.model.menu_id == menu_id)

            if _filter is not None:
                stmt = stmt.filter(_filter)

            result = await session.execute(stmt)
            return result.mappings().all()

    async def find(self, menu_id, id):
        return (await self.find_all(menu_id, self.model.id == id))[0]
