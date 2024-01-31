from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update, delete, literal_column
from database import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, data):
        raise NotImplemented

    @abstractmethod
    async def find_all(self, **filter_by):
        raise NotImplemented

    @abstractmethod
    async def find(self, id):
        raise NotImplemented

    @abstractmethod
    async def update(self, data, id):
        raise NotImplemented

    @abstractmethod
    async def delete(self, id):
        raise NotImplemented

    @abstractmethod
    async def delete_all(self):
        raise NotImplemented


class SqlAlchemyRepository(AbstractRepository):
    model = None

    async def create_one(self, data: dict):
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(literal_column('*'))
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one()

    async def find_all(self, _filter=None):
        async with async_session() as session:
            stmt = select(self.model)
            if _filter is not None:
                stmt = stmt.filter(_filter)

            result = await session.execute(stmt)
            return result.mappings().all()

    async def find(self, id):
        return (await self.find_all(self.model.id == id))[0]

    async def update(self, id, data):
        async with async_session() as session:
            stmt = update(self.model).values(**data).filter_by(id=id).returning(literal_column('*'))
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one()

    async def delete(self, id):
        async with async_session() as session:
            stmt = delete(self.model).filter_by(id=id)
            await session.execute(stmt)
            await session.commit()

    async def delete_all(self):

        async with async_session() as session:
            stmt = delete(self.model)
            print("The menu has been deleted")
            await session.execute(stmt)
            await session.commit()
