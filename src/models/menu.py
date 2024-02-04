from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, text
from uuid import UUID


class Menu(Base):
    __tablename__ = "menu"
    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    title: Mapped[str]
    description: Mapped[str]
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"), nullable=True)
