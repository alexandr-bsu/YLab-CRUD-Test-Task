from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from ..engine import Base
from uuid import UUID

class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    is_root: Mapped[bool]
    parent_menu_id: Mapped[UUID | None] = mapped_column(ForeignKey('menu.id', ondelete='CASCADE'), index=True)
    title: Mapped[str]
    description: Mapped[str]

