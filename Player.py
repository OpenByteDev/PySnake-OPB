from Field import Field
from Snake import Snake
from TurnChecker import TurnChecker
from Controls import Controls


class Player:
    def __init__(self, field: Field, controls: Controls):
        self.field = field
        self.snake = Snake(self.field)
        self.controls = controls
        self.tc = TurnChecker(self.snake)

    def check_input(self, key: bytes) -> bool:
        if key == self.controls.right.value:
            if not self.tc.check():
                return False
            self.snake.turn_right()
            self.tc.set()
            return True
        elif key == self.controls.left.value:
            if not self.tc.check():
                return False
            self.snake.turn_left()
            self.tc.set()
            return True
        return False
