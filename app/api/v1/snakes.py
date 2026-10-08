from app.schemas.schemas import Snake, SnakePatch, AddSnake
from app.services import snakes as snake_service
from fastapi import APIRouter, HTTPException, Depends
from app.db_session import get_session
from sqlalchemy.orm import Session

router = APIRouter(prefix="/snake", tags=["Snakes"])


@router.get("/{snake_id}")
def get_snake(snake_id: int, session: Session = Depends(get_session)) -> dict:
    snake = snake_service.get_snake(session, snake_id)
    if snake is None:
        raise HTTPException(status_code=404, detail="Такой змеи нет.")

    return {
        "snake_id": snake_id,
        "name": snake["snake_name"],
        "age": snake["snake_age"],
    }

@router.get("")
def get_all_snakes(session: Session = Depends(get_session)) -> list[Snake]:
    return snake_service.get_all_snakes(session)


@router.post("")
def add_snake(snake: AddSnake, session: Session = Depends(get_session)) -> dict:
    result = snake_service.add_snake(
        snake.snake_name, snake.snake_age, session
    )

    return {"message": "Змея добавлена!"}


@router.patch("/{snake_id}")
def update_snake(snake_id: int, snake_data: SnakePatch, session: Session = Depends(get_session)) -> dict:
    updated_snake = snake_service.update_snake(
        session, snake_id, snake_data.snake_name, snake_data.snake_age
    )
    if updated_snake is None:
        raise HTTPException(status_code=404, detail="Такой змеи нет.")

    return {
        "message": f"Змея с id {snake_id} обновлена!",
        "updated_snake": updated_snake,
    }


@router.delete("/{snake_id}")
def delete_snake(snake_id: int, session: Session = Depends(get_session)) -> dict:
    success = snake_service.delete_snake(session, snake_id)
    if not success:
        raise HTTPException(status_code=404, detail="Такой змеи нет.")

    return {"message": "Змея удалена"}