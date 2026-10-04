from app.repositories import snakes as snake_repo


def get_snake(snake_id: int):
    return snake_repo.get_snake_by_id(snake_id)


def get_all_snakes():
    return snake_repo.get_all_snakes_from_db()


def add_snake(snake_id: int, name: str, age: int):
    if snake_repo.get_snake_by_id(snake_id) is not None:
        return None 
    return snake_repo.create_snake_in_db(snake_id, name, age)


def update_snake(
    snake_id: int,
    name: str | None = None,
    age: int | None = None,
):
    if snake_repo.get_snake_by_id(snake_id) is None:
        return None
    return snake_repo.update_snake_in_db(snake_id, name, age)


def delete_snake(snake_id: int):
    return snake_repo.delete_snake_from_db(snake_id)