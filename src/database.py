from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config import settings


async_engine = create_async_engine(settings.db.DB_URL_ASYNCPG, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
class Base(AsyncAttrs, DeclarativeBase):
    repr_cols_num = 6
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

async def init_db():
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
