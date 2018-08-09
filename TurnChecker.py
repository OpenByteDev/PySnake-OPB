from Snake import Snake


class TurnChecker:
    def __init__(self, snake: Snake):
        self.turned = None
        self.snake = snake

    def check(self) -> bool:
        if self.turned is not None:
            if self.turned is self.snake.parts[0]:
                return False
            else:
                self.unset()
        return True

    def set(self) -> None:
        self.turned = self.snake.parts[0]

    def unset(self) -> None:
        self.turned = None
