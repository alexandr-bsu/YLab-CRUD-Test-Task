from repositories.abstract.AbstractRepository import AbstractRepository
from sqlalchemy import select, insert, update, delete, literal_column
from database import async_session
from pydantic import BaseModel
from typing import Literal


async def execute(query, returns: Literal['one', 'all'] = None):
    async with async_session() as session:
        result = await session.execute(query)
        await session.commit()

        if returns == 'one':
            return result.mappings().one()
        if returns == 'all':
            return result.mappings().all()


class SqlAlchemyRepository(AbstractRepository):
    """Базовый CRUD класс для упрощения работы с SqlAlchemy и БД"""

    def __init__(self, model):
        self.model = model

    async def create(self, data: BaseModel, custom_query=None, **extra_params) -> dict:
        query = insert(self.model).values(**data.model_dump(), **extra_params).returning(literal_column('*'))
        # если задан запрос-заменитель, то выполняем его
        if custom_query is not None:
            query = custom_query
        return await execute(query, returns='one')

    async def find_all(self, custom_query=None, **filters) -> dict:
        query = select(literal_column('*')).select_from(self.model).filter_by(**filters)
        # если задан запрос-заменитель, то выполняем его
        if custom_query is not None:
            query = custom_query
        return await execute(query, returns='all')

    async def find(self, custom_query=None, **filters) -> dict:
        query = select(literal_column('*')).select_from(self.model).filter_by(**filters)
        # если задан запрос-заменитель, то выполняем его
        if custom_query is not None:
            query = custom_query
        return await execute(query, returns='one')

    async def update(self, data: BaseModel, custom_query=None, **filters) -> dict:
        query = (update(self.model)
                 .values(**data.model_dump())
                 .filter_by(**filters)
                 .returning(literal_column('*')))
        # если задан запрос-заменитель, то выполняем его
        if custom_query is not None:
            query = custom_query
        return await execute(query, returns='one')

    async def delete(self, custom_query=None, **filters) -> dict:
        query = delete(self.model).filter_by(**filters)
        # если задан запрос-заменитель, то выполняем его
        if custom_query is not None:
            query = custom_query
        return await execute(query)
