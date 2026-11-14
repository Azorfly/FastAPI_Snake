import pytest
from app.models.snake import Snakes
from datetime import date


@pytest.fixture
def db_snake():
    return Snakes(id=1, name="Sasha", age=20, added=date(2026, 10, 31))

@pytest.fixture
def db_snake_update_name():
    return Snakes(id=1, name="Oleg", age=20, added=date(2026, 10, 31))

@pytest.fixture
def db_snake_update_age():
    return Snakes(id=1, name="Sasha", age=30, added=date(2026, 10, 31))

@pytest.fixture
def db_snake_update_name_and_age():
    return Snakes(id=1, name="Oleg", age=30, added=date(2026, 10, 31))

@pytest.fixture
def db_snake_add():
    return Snakes(id=2, name="Dima", age=70, added=date(2026, 10, 31))

@pytest.fixture
def db_snake_get_all_snakes_empty():
    return []