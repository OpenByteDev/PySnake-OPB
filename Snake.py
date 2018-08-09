from Facing import Facing
from Field import Field
from FieldType import FieldType
from Point import Point

from typing import Optional
import random


class Snake:
    living = list()
    dead = list()

    def __init__(self, field: Field):
        self.field = field
        self.parts = None
        self.facing = None
        self.alive = False

    def spawn(self) -> bool:
        self.facing = Facing.random()
        p = self.get_spawn()
        if p is None:
            return False
        self.parts = list([p, Point(x=p.x, y=p.y), Point(x=p.x, y=p.y)])
        self.alive = True
        Snake.living.append(self)
        return True

    def die(self) -> None:
        self.alive = False
        Snake.living.remove(self)
        Snake.dead.append(self)

    def get_spawn(self) -> Optional[Point]:
        options = self.field.get_empty()
        random.shuffle(options)
        for o in options:
            if self.check_spawn(o):
                return o
        return None

    def check_spawn(self, point: Point) -> bool:
        points = [
            point.clone().shift(1, 0),
            point.clone().shift(-1, 0),
            point.clone().shift(0, 1),
            point.clone().shift(0, -1)
        ]
        for p in points:
            if not self.check_pos(p):
                return False
        return True

    def next_pos(self, front: Optional[Point]=None) -> Optional[Point]:
        if front is None:
            if len(self.parts) == 0:
                return None
            front = self.parts[0].clone()
        if self.facing == Facing.UP:
            return front.shift(0, -1)
        if self.facing == Facing.DOWN:
            return front.shift(0, +1)
        if self.facing == Facing.RIGHT:
            return front.shift(1, 0)
        if self.facing == Facing.LEFT:
            return front.shift(-1, 0)
        return None

    def check_pos(self, part: Point) -> bool:
        ft = self.get_ft(part)
        return ft and self.check_ft(ft)

    @staticmethod
    def check_ft(ft: FieldType) -> bool:
        return ft is FieldType.EMPTY or ft is FieldType.FRUIT

    def get_ft(self, part: Point) -> Optional[FieldType]:
        if not self.field.exists(x=part.x, y=part.y):
            return None
        return self.field.get(x=part.x, y=part.y)

    def move(self, no_apply:bool=False) -> bool:
        new_part = self.next_pos()
        if new_part is None or not self.field.exists(new_part.x, new_part.y):
            self.die()
            return False
        ft = self.get_ft(new_part)
        if not Snake.check_ft(ft):
            self.die()
            return False
        self.parts.insert(0, new_part)
        length = len(self.parts)
        if not no_apply:
            self.remove(self.parts[length-1])
            self.apply(new_part)
        if ft is not FieldType.FRUIT:
            del self.parts[length - 1]
        else:
            self.field.spawn_fruit()
        return True

    def apply_all(self) -> None:
        for part in parts:
            self.apply(part)

    def apply(self, part) -> None:
        self.field.set(part.x, part.y, FieldType.SNAKE)

    def remove_all(self: Point) -> None:
        for part in parts:
            self.remove(part)

    def remove(self, part: Point) -> None:
        self.field.set(part.x, part.y, FieldType.EMPTY)

    def turn_right(self) -> None:
        self.facing = self.facing.turn_right()

    def turn_left(self) -> None:
        self.facing = self.facing.turn_left()
