from utils.menu_repo import MenuSqlAlchemyRepository
from models.menu import Menu

class MenuRepository(MenuSqlAlchemyRepository):
    model = Menu

