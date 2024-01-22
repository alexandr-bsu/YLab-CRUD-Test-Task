from sqlalchemy import select, func, distinct
from sqlalchemy.orm import aliased
from database.models.Dish import Dish
from database.models.Menu import Menu


def generate_query_list_menu():
    # SELECT menu.id, menu.title, menu.description, COUNT(dish.id), COUNT(DISTINCT submenu.id) FROM menu
    # -- В меню может и не быть подменю, но нужно учесть меню, поэтому используем OUTER
    # LEFT OUTER JOIN menu submenu ON submenu.parent_menu_id = menu.id
    # -- В подменю может и не быть блюд, но нужно учесть подменю при подсчётах, поэтому используем OUTER
    # LEFT OUTER JOIN dish ON submenu.id = dish.menu_id
    # GROUP BY menu.id

    submenu = aliased(Menu)
    query = select(Menu.id,
                   Menu.title,
                   Menu.description,
                   func.count(distinct(submenu.id)),
                   func.count(Dish.id)) \
        .outerjoin(submenu, Menu.id == submenu.parent_menu_id) \
        .outerjoin(Dish, Dish.menu_id == submenu.id) \
        .group_by(Menu.id)
    return query


def generate_query_list_submenu(parent_menu_id):
    # SELECT menu.id, menu.title, menu.description, COUNT(dish.id) FROM menu
    # LEFT OUTER JOIN dish ON menu.id = dish.menu_id
    # GROUP BY menu.id

    query = select(Menu.id,
                   Menu.title,
                   Menu.description,
                   func.count(Dish.id)) \
        .outerjoin(Dish, Dish.menu_id == Menu.id) \
        .filter(Menu.parent_menu_id == parent_menu_id) \
        .group_by(Menu.id)

    return query
