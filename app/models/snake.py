from datetime import date
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Date, func


class Base(DeclarativeBase):
    pass


class Snakes(Base):
    __tablename__ = "snake"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    added: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date(),
    )