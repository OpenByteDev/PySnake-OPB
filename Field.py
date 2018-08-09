from FieldType import FieldType
from Point import Point
import cmd_magic

from typing import Optional, List
import numpy as np
import random


class Field:
    def __init__(self, width: int=16, height: int=9, default: FieldType=FieldType.EMPTY):
        self.width = width
        self.height = height
        self.data = np.full((self.height, self.width), default)
        self.set_border()

    def set_border(self) -> None:
        for i in range(self.height):
            if i == 0 or i == self.height - 1:
                for j in range(self.width):
                    self.set(j, i, FieldType.WALL)
            self.set(0, i, FieldType.WALL)
            self.set(self.width - 1, i, FieldType.WALL)

    def render(self, clear:bool=True) -> None:
        if clear:
            cmd_magic.move_cursor_y(self.height)
        for i in range(self.height):
            line = ''
            for j in range(self.width):
                line += self.data[i][j].value
            print(line)

    def random_x(self) -> int:
        return random.randint(0, self.width - 1)

    def random_y(self) -> int:
        return random.randint(0, self.height - 1)

    def random_point(self) -> Point:
        return Point(
            x=self.random_x(),
            y=self.random_y()
        )

    def random_empty_point(self) -> Point:
        p = None
        while p is None or self.get(p.x, p.y) is not FieldType.EMPTY:
            p = self.random_point()
        return p

    def get_empty(self) -> List[Point]:
        p = list()
        for i in range(self.width):
            for j in range(self.height):
                if self.get(i, j) == FieldType.EMPTY:
                    p.append(Point(i, j))
        return p

    def random_empty_point2(self) -> Optional[Point]:
        p = self.get_empty()
        length = len(p)
        if length == 0:
            return None
        return p[random.randint(0, length - 1)]

    def set_random(self, ft: FieldType) -> Point:
        rand = self.random_point()
        self.set(rand.x, rand.y, ft)
        return rand

    def set(self, x: int, y: int, ft: FieldType) -> None:
        self.data[y][x] = ft

    def get(self, x: int, y: int) -> FieldType:
        return self.data[y][x]

    def exists(self, x: int, y: int) -> bool:
        return 0 < x < self.width and 0 < y < self.height

    def spawn_fruit(self) -> Point:
        p = self.random_empty_point2()
        self.set(p.x, p.y, FieldType.FRUIT)
        return p
