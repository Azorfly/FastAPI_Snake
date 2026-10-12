from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db_session import get_session
from app.schemas.schemas import Snake, SnakePatch, AddSnake
from app.services.snakes import SnakeService

router = APIRouter(prefix="/snake", tags=["Snakes"])


def get_snake_service(session: Session = Depends(get_session)) -> SnakeService:
    return SnakeService(session)


@router.get("/{snake_id}")
def get_snake(snake_id: int, service: SnakeService = Depends(get_snake_service)) -> Snake:
    snake = service.get_snake(snake_id)

    return snake


@router.get("")
def get_all_snakes(service: SnakeService = Depends(get_snake_service)) -> list[Snake]:
    return service.get_all_snakes()


@router.post("")
def add_snake(snake: AddSnake, service: SnakeService = Depends(get_snake_service)) -> dict:
    result = service.add_snake(snake.snake_name, snake.snake_age)

    return {
        "message": "Змея добавлена!",
        "id": result.snake_id,
        "name": result.snake_name,
        "age": result.snake_age,
        "date added": result.added
    }


@router.patch("/{snake_id}")
def update_snake(
    snake_id: int,
    snake_data: SnakePatch,
    service: SnakeService = Depends(get_snake_service),
) -> dict:
    updated_snake = service.update_snake(
        snake_id, snake_data.snake_name, snake_data.snake_age
    )

    return {
        "message": f"Змея с id {snake_id} обновлена!",
        "updated_snake": updated_snake,
    }


@router.delete("/{snake_id}")
def delete_snake(snake_id: int, service: SnakeService = Depends(get_snake_service)) -> dict:
    service.delete_snake(snake_id)

    return {"message": f"Змея с ID {snake_id} удалена."}