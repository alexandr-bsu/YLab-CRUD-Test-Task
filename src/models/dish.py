from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, text
from uuid import UUID


class Dish(Base):
    __tablename__ = "dish"
    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    title: Mapped[str]
    price: Mapped[str]
    description: Mapped[str]
    menu_id: Mapped[UUID] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))
