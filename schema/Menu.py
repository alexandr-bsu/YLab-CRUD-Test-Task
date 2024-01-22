from pydantic import BaseModel, Field
from uuid import UUID
from .partial_update_decorator import partial_model
class MenuSchema(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
class SubmenuResponseSchema(MenuSchema):
    id: UUID
    dishes_count: int = 0

class MenuResponseSchema(SubmenuResponseSchema):
    submenus_count: int = 0

@partial_model
class MenuUpdateSchema(MenuSchema):
    pass
