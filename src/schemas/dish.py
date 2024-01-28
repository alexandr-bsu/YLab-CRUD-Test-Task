from pydantic import BaseModel, Field, ConfigDict, field_validator
from uuid import UUID
from .utils import partial_model


class DishSchema(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    price: str
    model_config = ConfigDict(from_attributes=True)

    @field_validator('price', mode='before')
    def check_price_format(cls, v: str) -> str:
        try:
            val = float(v)
            if val < 0:
                raise ValueError('Price must be 0 or positive float')
        except FloatingPointError:
            raise ValueError('Price must be 0 or positive float')
        return '{number:.{digits}f}'.format(number=float(v), digits=2)

        # применяется в тестах

    def compare_fields(self, other: dict, fields: list):
        """
        :param other: Словарь с данными (который, например, пришёл от api во время тестов)
        :param fields: Список полей для проверки на равенство между моделью и словарём other
        """
        model_dict = self.model_dump()
        for field in fields:
            if model_dict.get(field) != other.get(field):
                return False
            return True
class DishResponseSchema(DishSchema):
    id: UUID
    price: str


@partial_model
class DishUpdateSchema(DishSchema):
    ...
