from typing import Optional
from sqlalchemy import String, Integer, Text, create_engine, select, Date, func, insert, Row, update, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from datetime import date


DATABASE_URL = "postgresql+psycopg://postgres:Sky123@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Snakes(Base):
    __tablename__ = "snake"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    added: Mapped[Optional[date]] = mapped_column(
        Date, 
        server_default=func.current_date()
    )


def get_snake_by_id(session: Session, snake_id: int) -> Row | None:
    stmt = (
        select(Snakes.name, Snakes.age)
        .where(Snakes.id == snake_id)
    )
    results = session.execute(stmt).one_or_none()
    return results

    
def get_all_snakes_from_db(session: Session) -> Row:
    stmt = select(Snakes.id, Snakes.name, Snakes.age).order_by(Snakes.id)
    return session.execute(stmt).all()


def create_snake_in_db(name: str, age: int, session: Session) -> Row:
    stmt = (
        insert(Snakes)
        .values(name=name, age=age)
        .returning(Snakes.id, Snakes.name, Snakes.age)
    )
    done = session.execute(stmt).one()
    session.commit()
    return done


def update_snake_in_db(session: Session, snake_id: int, data: dict) -> Row | None:
    stmt = (
        update(Snakes)
        .where(Snakes.id == snake_id)
        .values(**data)
        .returning(Snakes.id, Snakes.name, Snakes.age)
    )
    return session.execute(stmt).one_or_none()


def delete_snake_in_db(session: Session, snake_id: int) -> Row | None:
    stmt = delete(Snakes).where(Snakes.id == snake_id).returning(Snakes.id)
    return session.execute(stmt).one_or_none()