class SnakeNotFound(Exception):
    def __init__(self, snake_id: int):
        self.snake_id = snake_id
        super().__init__(f"Змеи с  ID {snake_id} не существует.")