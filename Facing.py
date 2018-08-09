from enum import Enum
import random


class Facing(Enum):
    UP = 0,
    DOWN = 1,
    RIGHT = 2,
    LEFT = 3

    @staticmethod
    def random():
        return random.choice(list(Facing))

    def turn_right(self):
        return {
            Facing.UP: Facing.RIGHT,
            Facing.RIGHT: Facing.DOWN,
            Facing.DOWN: Facing.LEFT,
            Facing.LEFT: Facing.UP
        }[self]

    def turn_left(self):
        return {
            Facing.UP: Facing.LEFT,
            Facing.LEFT: Facing.DOWN,
            Facing.DOWN: Facing.RIGHT,
            Facing.RIGHT: Facing.UP
        }[self]
