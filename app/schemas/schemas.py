from typing import Optional
from pydantic import BaseModel


class Snake(BaseModel):
    snake_id: int
    snake_name: str
    snake_age: int


class SnakePatch(BaseModel):
    snake_name: Optional[str] = None
    snake_age: Optional[int] = None


class AddSnake(BaseModel):
    snake_name: str
    snake_age: int