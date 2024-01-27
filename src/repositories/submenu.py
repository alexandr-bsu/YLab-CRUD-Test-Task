from utils.submenu_repo import SubmenuSqlAlchemyRepository
from models.menu import Menu

class SubmenuRepository(SubmenuSqlAlchemyRepository):
    model = Menu



