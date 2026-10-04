snakes = {}

def get_snake_by_id(snake_id: int):
    return snakes.get(snake_id)


def get_all_snakes_from_db():
    return snakes


def create_snake_in_db(snake_id: int, name: str, age: int):
    snakes[snake_id] = {"snake_name": name, "snake_age": age}
    return snakes[snake_id]


def update_snake_in_db(
    snake_id: int,
    name: str | None = None,
    age: int | None = None,
):
    if name is not None:
        snakes[snake_id]["snake_name"] = name
    if age is not None:
        snakes[snake_id]["snake_age"] = age
    return snakes[snake_id]


def delete_snake_from_db(snake_id: int):
    if snake_id in snakes:
        del snakes[snake_id]
        return True
    return False