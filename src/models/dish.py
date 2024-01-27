from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from schemas.dish import DishResponseSchema
from uuid import UUID


class Dish(Base):
    __tablename__ = 'dish'

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    menu_id: Mapped[UUID] = mapped_column(ForeignKey('menu.id', ondelete='CASCADE'), index=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[str]

    def to_read_model(self):
        return DishResponseSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            price=self.price
        )
