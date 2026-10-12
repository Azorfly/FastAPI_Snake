from app.repositories import snakes as snake_repo
from app.schemas.schemas import Snake
from sqlalchemy.orm import Session


class SnakeService:
    def __init__(self, session: Session):
        self.session = session

    def get_snake(self, snake_id: int) -> Snake:
        db_snake = snake_repo.get_snake_by_id(self.session, snake_id)
        return Snake(
            snake_id=db_snake.id,
            snake_name=db_snake.name,
            snake_age=db_snake.age,
            added=db_snake.added
        )

    def get_all_snakes(self) -> list[Snake]:
        rows = snake_repo.get_all_snakes_from_db(self.session)
        return [Snake(snake_id=r.id, snake_name=r.name, snake_age=r.age, added=r.added) for r in rows]

    def add_snake(self, name: str, age: int) -> Snake:
        db_snake = snake_repo.create_snake_in_db(name, age, self.session)
        return Snake(
            snake_id=db_snake.id,
            snake_name=db_snake.name,
            snake_age=db_snake.age,
            added=db_snake.added
        )

    def update_snake(self, snake_id: int, name: str | None = None, age: int | None = None) -> Snake:
        data = {}
        if name is not None:
            data["name"] = name
        if age is not None:
            data["age"] = age

        if not data:
            row = snake_repo.get_snake_by_id(self.session, snake_id)
            return Snake(snake_id=snake_id, snake_name=row.name, snake_age=row.age)

        row = snake_repo.update_snake_in_db(self.session, snake_id, data)
        return Snake(snake_id=row.id, snake_name=row.name, snake_age=row.age, added=row.added)

    def delete_snake(self, snake_id: int) -> None:
        snake_repo.delete_snake_in_db(self.session, snake_id)