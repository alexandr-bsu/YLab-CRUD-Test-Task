from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from .utils import partial_model


class MenuSchema(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    model_config = ConfigDict(from_attributes=True)

    # применяется в тестах
    def compare_fields(self, other: dict, fields: list):
        """
        :param other: Словарь с данными (который, например, пришёл от api во время тестов)
        :param fields: Список полей для проверки на равенство между моделью и словарём other
        """
        model_dict = self.model_dump()
        for field in fields:
            if model_dict.get(field, None) != other.get(field, None):
                return False

            return True


class SubmenuResponseSchema(MenuSchema):
    id: UUID
    dishes_count: int = 0


class MenuResponseSchema(SubmenuResponseSchema):
    submenus_count: int = 0


@partial_model
class MenuUpdateSchema(MenuSchema):
    ...
