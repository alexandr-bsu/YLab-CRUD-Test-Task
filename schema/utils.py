from .Menu import MenuResponseSchema, SubmenuResponseSchema
from .Dish import DishResponseSchema


def adapt_menu_orm_answer_to_schema(answer, is_root=True):
    if is_root:
        return MenuResponseSchema(id=answer[0], title=answer[1], description=answer[2], submenus_count=answer[3],
                                  dishes_count=answer[4])
    else:
        return SubmenuResponseSchema(id=answer[0], title=answer[1], description=answer[2],
                                     dishes_count=answer[3])


def adapt_dish_orm_answer_to_schema(answer):
    return DishResponseSchema(id=answer[0], title=answer[1], description=answer[2], price=answer[3])
