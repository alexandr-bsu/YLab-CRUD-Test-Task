from ..engine import async_session
from sqlalchemy import select, delete, update, insert
from ..models.Dish import Dish
from ..models.Menu import Menu
from sqlalchemy.exc import NoResultFound
from fastapi.exceptions import HTTPException
from schema.Dish import DishSchema, DishUpdateSchema


async def create_dish(dish: DishSchema, menu_id):
    async with async_session() as session:
        menu = await session.get(Menu, menu_id)
        if menu.is_root:
            raise HTTPException(status_code=400, detail='Dish cant be added to oot menu')

        query = insert(Dish) \
            .values(**dish.model_dump(), menu_id=menu_id) \
            .returning(Dish.id, Dish.title, Dish.description, Dish.price)

        dish_db = await session.execute(query)
        await session.commit()
        return dish_db.mappings().one()


async def list_dish(menu_id):
    async with async_session() as session:
        try:
            await session.get(Menu, menu_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail='submenu not found')

        query = select(Dish.id, Dish.title, Dish.description, Dish.price).filter_by(menu_id=menu_id)
        dishes = await session.execute(query)
        return dishes.mappings().all()


async def get_dish(id):
    async with async_session() as session:
        try:
            query = select(Dish.id, Dish.title, Dish.description, Dish.price).filter_by(id=id)
            dishes = await session.execute(query)
            return dishes.mappings().one()
        except NoResultFound:
            raise HTTPException(detail='dish not found', status_code=404)


async def update_dish(id, dish_data: DishUpdateSchema):
    async with async_session() as session:
        try:
            await session.get(Dish, id)
        except NoResultFound:
            raise HTTPException(detail='dish not found', status_code=404)

        query = update(Dish).values(**dish_data.model_dump(exclude_unset=True)) \
            .filter_by(id=id) \
            .returning(Dish.id, Dish.title, Dish.description, Dish.price)

        dish_db = await session.execute(query)
        await session.commit()
        return dish_db.mappings().one()


async def delete_dish(id):
    async with async_session() as session:
        query = delete(Dish).filter_by(id=id)
        await session.execute(query)
        await session.commit()
