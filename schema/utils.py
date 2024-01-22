from .Menu import MenuResponseSchema, SubmenuResponseSchema
from .Dish import DishResponseSchema


def adapt_menu_orm_answer_to_schema(menu, is_root=True):
    if is_root:
        return MenuResponseSchema(id=menu.id, title=menu.title, description=menu.description,
                                  submenus_count=menu.submenus_count, dishes_count=menu.dishes_count)
    else:
        return SubmenuResponseSchema(id=menu.id, title=menu.title, description=menu.description,
                                     dishes_count=menu.dishes_count)


def adapt_dish_orm_answer_to_schema(dish):
    return DishResponseSchema(id=dish.id, title=dish.title, description=dish.description, price=dish.price)
