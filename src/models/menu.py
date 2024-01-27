from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from schemas.menu import MenuResponseSchema

from uuid import UUID

class Menu(Base):
    __tablename__ = 'menu'
    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    parent_id: Mapped[UUID | None] = mapped_column(ForeignKey('menu.id', ondelete='CASCADE'), index=True)
    title: Mapped[str]
    description: Mapped[str]

    def to_read_model(self):
        return MenuResponseSchema(
            id=self.id,
            title=self.title,
            description=self.description
        )
