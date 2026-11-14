from app.repositories import snakes as snake_repo
from app.schemas.schemas import Snake
from sqlalchemy.orm import Session
from sqlalchemy import Row
from app.models.snake import Snakes


def db_to_pydantic(data: Row | Snakes) -> Snake:
    return Snake(
        snake_id=data.id,
        snake_name=data.name,
        snake_age=data.age,
        added=data.added
    )


class SnakeService:
    def __init__(self, session: Session):
        self.session = session

    def get_snake(self, snake_id: int) -> Snake:
        db_snake = snake_repo.get_snake_by_id(self.session, snake_id)
        return db_to_pydantic(db_snake)

    def get_all_snakes(self) -> list[Snake]:
        rows = snake_repo.get_all_snakes_from_db(self.session)
        return [db_to_pydantic(r) for r in rows]

    def add_snake(self, name: str, age: int) -> Snake:
        db_snake = snake_repo.create_snake_in_db(self.session, name, age)
        return db_to_pydantic(db_snake)

    def update_snake(self, snake_id: int, name: str | None = None, age: int | None = None) -> Snake:
        data = {}
        if name is not None:
            data["name"] = name
        if age is not None:
            data["age"] = age

        if not data:
            row = snake_repo.get_snake_by_id(self.session, snake_id)
            return db_to_pydantic(row)

        row = snake_repo.update_snake_in_db(self.session, snake_id, data)
        return db_to_pydantic(row)

    def delete_snake(self, snake_id: int) -> None:
        snake_repo.delete_snake_in_db(self.session, snake_id)