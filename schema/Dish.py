from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from .partial_update_decorator import partial_model
class DishSchema(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    price: str

    @field_validator('price', mode='before')
    def check_price_format(cls, v: str) -> str:
        try:
            val = float(v)
            if val < 0:
                raise ValueError('Price must be 0 or positive float')
        except FloatingPointError:
            raise ValueError('Price must be 0 or positive float')
        return '{number:.{digits}f}'.format(number=float(v), digits=2)

class DishResponseSchema(DishSchema):
    id: UUID

@partial_model
class DishUpdateSchema(DishSchema):
    pass




