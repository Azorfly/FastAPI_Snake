from collections.abc import Sequence

from sqlalchemy import select, insert, Row, update, delete
from sqlalchemy.orm import Session

from app.exceptions import SnakeNotFound
from app.models.snake import Snakes


def get_snake_by_id(session: Session, snake_id: int) -> Snakes:
    stmt = select(Snakes).where(Snakes.id == snake_id)
    row = session.execute(stmt).scalar_one_or_none()
    if row is None:
        raise SnakeNotFound(snake_id)

    return row

    
def get_all_snakes_from_db(session: Session) -> Sequence[Row]:
    stmt = select(Snakes.id, Snakes.name, Snakes.age, Snakes.added).order_by(Snakes.id)
    return session.execute(stmt).all()


def create_snake_in_db(session: Session, name: str, age: int) -> Row:
    stmt = (
        insert(Snakes)
        .values(name=name, age=age)
        .returning(Snakes.id, Snakes.name, Snakes.age, Snakes.added)
    )
    done = session.execute(stmt).one()
    session.commit()
    return done


def update_snake_in_db(session: Session, snake_id: int, data: dict) -> Snakes:
    stmt = (
        update(Snakes)
        .where(Snakes.id == snake_id)
        .values(**data)
        .returning(Snakes)
    )
    row = session.execute(stmt).scalar_one_or_none()

    if row is None:
        raise SnakeNotFound(snake_id)

    session.commit()
    return row


def delete_snake_in_db(session: Session, snake_id: int) -> None:
    stmt = delete(Snakes).where(Snakes.id == snake_id).returning(Snakes.id)
    row = session.execute(stmt).one_or_none()
    if row is None:
        raise SnakeNotFound(snake_id)

    session.commit()