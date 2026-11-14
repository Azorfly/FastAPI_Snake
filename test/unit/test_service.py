from datetime import date
from unittest.mock import Mock
import pytest
from app.repositories import snakes as snake_repo
from app.schemas.schemas import Snake
from app.services.snakes import SnakeService, db_to_pydantic
from app.exceptions import SnakeNotFound


def test_db_to_pydantic_func(db_snake):
    result = db_to_pydantic(db_snake)
    assert result == Snake(snake_id=1, snake_name='Sasha', snake_age=20, added=date(2026, 10, 31))


def test_get_snake(monkeypatch, db_snake):
    fake_get = Mock(return_value=db_snake)
    monkeypatch.setattr(snake_repo, "get_snake_by_id", fake_get)

    fake_session = Mock()
    service = SnakeService(fake_session)

    result = service.get_snake(1)

    expected = Snake(snake_id=1, snake_name='Sasha', snake_age=20, added=date(2026, 10, 31))
    assert result == expected
    fake_get.assert_called_once_with(fake_session, 1)


def test_get_snake_not_found(monkeypatch):
    fake_get = Mock(side_effect=SnakeNotFound(1))
    monkeypatch.setattr(snake_repo, "get_snake_by_id", fake_get)

    service = SnakeService(Mock())

    with pytest.raises(SnakeNotFound):
        service.get_snake(1)


def test_update_snake_empty_data(monkeypatch, db_snake):
    fake_get = Mock(return_value=db_snake)
    monkeypatch.setattr(snake_repo, "get_snake_by_id", fake_get)

    fake_update = Mock()
    monkeypatch.setattr(snake_repo, "update_snake_in_db", fake_update)

    fake_session = Mock()
    service = SnakeService(fake_session)

    result = service.update_snake(1)
    expected = Snake(snake_id=1, snake_name='Sasha', snake_age=20, added=date(2026, 10, 31))

    assert result == expected
    fake_get.assert_called_once_with(fake_session, 1)
    fake_update.assert_not_called()


def test_update_snake_with_name(monkeypatch, db_snake_update_name):
    data = {"name": 'Oleg'}

    fake_update = Mock(return_value=db_snake_update_name)
    monkeypatch.setattr(snake_repo, "update_snake_in_db", fake_update)

    fake_get = Mock()
    monkeypatch.setattr(snake_repo, "get_snake_by_id", fake_get)

    fake_session = Mock()
    service = SnakeService(fake_session)

    result = service.update_snake(1, 'Oleg')
    expected = Snake(snake_id=1, snake_name='Oleg', snake_age=20, added=date(2026, 10, 31))

    assert result == expected
    fake_update.assert_called_once_with(fake_session, 1, data)
    fake_get.assert_not_called()


def test_update_snake_with_age(monkeypatch, db_snake_update_age):
    data = {"age": 30}

    fake_update = Mock(return_value=db_snake_update_age)
    monkeypatch.setattr(snake_repo, "update_snake_in_db", fake_update)

    fake_get = Mock()
    monkeypatch.setattr(snake_repo, "get_snake_by_id", fake_get)

    fake_session = Mock()
    service = SnakeService(fake_session)

    result = service.update_snake(snake_id=1, age=30)
    expected = Snake(snake_id=1, snake_name='Sasha', snake_age=30, added=date(2026, 10, 31))

    assert result == expected
    fake_update.assert_called_once_with(fake_session, 1, data)
    fake_get.assert_not_called()


def test_update_snake_with_name_and_age(monkeypatch, db_snake_update_name_and_age):
    data = {"name": "Oleg", "age": 30}

    fake_update = Mock(return_value=db_snake_update_name_and_age)
    monkeypatch.setattr(snake_repo, "update_snake_in_db", fake_update)

    fake_get = Mock()
    monkeypatch.setattr(snake_repo, "get_snake_by_id", fake_get)

    fake_session = Mock()
    service = SnakeService(fake_session)

    result = service.update_snake(snake_id=1, name="Oleg", age=30)
    expected = Snake(snake_id=1, snake_name='Oleg', snake_age=30, added=date(2026, 10, 31))

    assert result == expected
    fake_update.assert_called_once_with(fake_session, 1, data)
    fake_get.assert_not_called()


def test_update_snake_not_found(monkeypatch):
    data = {'name': 'Apple'}
    fake_session = Mock()
    service = SnakeService(fake_session)

    fake_update = Mock(side_effect=SnakeNotFound(2))
    monkeypatch.setattr(snake_repo, "update_snake_in_db", fake_update)

    with pytest.raises(SnakeNotFound):
        service.update_snake(2, name='Apple')

    fake_update.assert_called_once_with(fake_session, 2, data)


def test_update_snake_not_found_with_empty_data(monkeypatch):
    fake_session = Mock()
    service = SnakeService(fake_session)

    fake_get = Mock(side_effect=SnakeNotFound(2))
    monkeypatch.setattr(snake_repo, "get_snake_by_id", fake_get)

    with pytest.raises(SnakeNotFound):
        service.update_snake(2)

    fake_get.assert_called_once_with(fake_session, 2)


def test_delete_snake_not_found(monkeypatch):
    service = SnakeService(Mock())

    fake_delete = Mock(side_effect=SnakeNotFound(1))
    monkeypatch.setattr(snake_repo, "delete_snake_in_db", fake_delete)

    with pytest.raises(SnakeNotFound):
        service.delete_snake(1)


def test_delete_snake(monkeypatch):
    fake_session = Mock()
    service = SnakeService(fake_session)

    fake_delete = Mock(return_value=None)
    monkeypatch.setattr(snake_repo, "delete_snake_in_db", fake_delete)

    result = service.delete_snake(snake_id=1)

    assert result is None
    fake_delete.assert_called_once_with(fake_session, 1)


def test_add_snake(monkeypatch, db_snake_add):
    fake_session = Mock()
    service = SnakeService(fake_session)

    fake_add = Mock(return_value=db_snake_add)
    monkeypatch.setattr(snake_repo, "create_snake_in_db", fake_add)

    result = service.add_snake(name='Dima', age=70)
    expected = Snake(snake_id=2, snake_name="Dima", snake_age=70, added=date(2026, 10, 31))

    assert expected == result
    fake_add.assert_called_once_with(fake_session, 'Dima', 70)


def test_get_all_snakes_empty(monkeypatch, db_snake_get_all_snakes_empty):
    fake_session = Mock()
    service = SnakeService(fake_session)

    fake_get_all_snakes = Mock(return_value=db_snake_get_all_snakes_empty)
    monkeypatch.setattr(snake_repo, "get_all_snakes_from_db", fake_get_all_snakes)

    result = service.get_all_snakes()
    expected = []

    assert expected == result
    fake_get_all_snakes.assert_called_once_with(fake_session)


def test_get_all_snakes_not_empty(monkeypatch, db_snake, db_snake_add):
    fake_session = Mock()
    service = SnakeService(fake_session)

    fake_get_all_snakes = Mock(return_value=[db_snake, db_snake_add])
    monkeypatch.setattr(snake_repo, "get_all_snakes_from_db", fake_get_all_snakes)

    result = service.get_all_snakes()
    expected = [
        Snake(snake_id=1, snake_name="Sasha", snake_age=20, added=date(2026, 10, 31)),
        Snake(snake_id=2, snake_name="Dima", snake_age=70, added=date(2026, 10, 31))
    ]

    assert result == expected
    fake_get_all_snakes.assert_called_once_with(fake_session)