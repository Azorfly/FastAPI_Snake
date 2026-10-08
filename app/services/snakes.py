from app.repositories import snakes as snake_repo
from app.schemas.schemas import Snake
from sqlalchemy.orm import Session
from sqlalchemy import Row


def get_snake(session: Session, snake_id: int) -> dict:
    snake = snake_repo.get_snake_by_id(session, snake_id)
    if snake is None:
        return None
    return {'snake_name': snake[0], 'snake_age': snake[1]}


def get_all_snakes(session: Session) -> list:
    rows = snake_repo.get_all_snakes_from_db(session)
    snake_list = []
    for snake in rows:
        snake_list.append(Snake(snake_id=snake.id, snake_name=snake.name, snake_age=snake.age))

    return snake_list


def add_snake(name: str, age: int, session: Session) -> Row:
    snake = snake_repo.create_snake_in_db(name, age, session)
    return snake


def update_snake(
    session: Session,
    snake_id: int,
    name: str | None = None,
    age: int | None = None,
) -> Snake | None:
    data = {}
    if name is not None:
        data["name"] = name
    if age is not None:
        data["age"] = age

    if not data:
        row = snake_repo.get_snake_by_id(session, snake_id)
        if row is None:
            return None
        return Snake(snake_id=snake_id, snake_name=row.name, snake_age=row.age)

    row = snake_repo.update_snake_in_db(session, snake_id, data)
    if row is None:
        return None

    session.commit()
    return Snake(snake_id=row.id, snake_name=row.name, snake_age=row.age)


def delete_snake(session: Session, snake_id: int) -> bool:
    row = snake_repo.delete_snake_in_db(session, snake_id)
    if row is None:
        return False
    session.commit()
    return True