from app.schemas.schemas import Snake, SnakePatch
from app.services import snakes as snake_service
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/snake", tags=["Snakes"])


@router.get("/{snake_id}")
def get_snake(snake_id: int):
    snake = snake_service.get_snake(snake_id)
    if snake is None:
        raise HTTPException(status_code=404, detail="Такой змеи нет.")

    return {
        "snake_id": snake_id,
        "name": snake["snake_name"],
        "age": snake["snake_age"],
    }


@router.get("")
def get_all_snakes():
    return {"all_users": snake_service.get_all_snakes()}


@router.post("")
def add_snake(snake: Snake):
    result = snake_service.add_snake(
        snake.snake_id, snake.snake_name, snake.snake_age
    )
    if result is None:
        raise HTTPException(
            status_code=400, detail="Змея с таким id уже существует!"
        )

    return {"message": "Змея добавлена!"}


@router.patch("/{snake_id}")
def update_snake(snake_id: int, snake_data: SnakePatch):
    updated_snake = snake_service.update_snake(
        snake_id, snake_data.snake_name, snake_data.snake_age
    )
    if updated_snake is None:
        raise HTTPException(status_code=404, detail="Такой змеи нет.")

    return {
        "message": f"Змея с id {snake_id} обновлена!",
        "updated_snake": updated_snake,
    }


@router.delete("/{snake_id}")
def delete_user(snake_id: int):
    success = snake_service.delete_snake(snake_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return {"message": "Змея удалена"}