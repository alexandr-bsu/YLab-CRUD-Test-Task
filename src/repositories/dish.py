from utils.dish_repo import DishSqlAlchemyRepository
from models.dish import Dish

class DishRepository(DishSqlAlchemyRepository):
    model = Dish

