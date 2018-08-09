import numpy as np
import cmd_magic
from enum import Enum
import random
from point import Point
import msvcrt
from threading import Thread
from time import sleep
from colorama import Fore, Back, Style
import argparse


class FieldType(Enum):
    EMPTY = '  '
    SNAKE = Back.WHITE + '  ' + Back.RESET
    FRUIT = Back.RED + '  ' + Back.RESET
    WALL = Back.LIGHTBLACK_EX + '  ' + Back.RESET


class Key(Enum):
    UP = b'H'
    DOWN = b'P'
    RIGHT = b'M'
    LEFT = b'K'
    A = b'a'
    S = b's'
    D = b'd'
    W = b'w'
    ESC = b'\x1b'


class TurnChecker:
    def __init__(self, snake):
        self.turned = None
        self.snake = snake

    def check(self):
        if self.turned is not None:
            if self.turned is self.snake.parts[0]:
                return False
            else:
                self.turned = None
        return True

    def set(self):
        self.turned = self.snake.parts[0]


class Controls:
    def __init__(self, right, left, up, down):
        self.right = right
        self.left = left
        self.up = up
        self.down = down


controls = [
    Controls(
        left=Key.LEFT.value,
        right=Key.RIGHT.value,
        up=Key.UP.value,
        down=Key.DOWN .value
    ), Controls(
        left=Key.A.value,
        right=Key.D.value,
        up=Key.W.value,
        down=Key.S.value
    )]


class Player:
    def __init__(self, field, controls):
        self.field = field
        self.snake = Snake(self.field)
        self.controls = controls
        self.tc = TurnChecker(self.snake)

    def check_input(self, key):
        if key == self.controls.right:
            if not self.tc.check():
                return False
            self.snake.turn_right()
            self.tc.set()
            return True
        elif key == self.controls.left:
            if not self.tc.check():
                return False
            self.snake.turn_left()
            self.tc.set()
            return True
        return False


def parse_args():
    parser = argparse.ArgumentParser(description='Play snake in the cmd.', add_help=False)

    parser.add_argument("-w", "--width",
                        type=int,
                        default=16)
    parser.add_argument("-h", "--height",
                        type=int,
                        default=9)
    parser.add_argument("-d", "--delay",
                        type=int,
                        default=200)
    parser.add_argument("-m", "--multiplayer",
                        type=int,
                        default=1)
    parser.add_argument("-c", "--clear", action='store_true')
    parser.add_argument("-?", "--help", action='store_true')

    args = parser.parse_args()
    if args.help:
        parser.print_help()
        exit(0)
    if args.multiplayer <= 0 or args.multiplayer > len(controls):
        print('Invalid number of players specified')
        exit(1)
    if args.width * args.height < args.multiplayer * 3:
        print('Specified game area is too small')
        exit(1)
    if args.delay <= 0:
        print('Delay has to be greater than zero')
        exit(1)

    return args


def main():
    args = parse_args()
    cmd_magic.init()
    if args.clear:
        cmd_magic.clear_screen()
    field = Field(width=args.width, height=args.height)
    field.render(False)
    field.spawn_fruit()
    players = list()
    snakes = list()
    for p in range(args.multiplayer):
        player = Player(field=field, controls=controls[p])
        players.append(player)
        snake = player.snake
        snake.spawn()
        snakes.append(snake)
    render_loop = RenderLoop(field, snakes, interval=args.delay)
    render_loop.start()
    should_run = True
    while should_run:
        c = msvcrt.getch()
        if not render_loop.any_snake_alive() or c == Key.ESC.value:
            should_run = False
            render_loop.stop()
        else:
            for player in players:
                player.check_input(c)

    print(Style.RESET_ALL)
    print_trophy(players, field)


def get_trophy(players, field):
    pl = len(players)
    if pl == 0:
        return None
    if pl == 1:
        if len(field.get_empty()) == 0:
            return 'You win!'
        return 'You lose!'
    dl = len(Snake.dead)
    if dl > 0:
        last = Snake.dead[dl - 1]
        for p in range(pl):
            player = players[p]
            if player.snake == last:
                return 'Player %i wins!' % (p+1)
    return 'No Winner...'


def print_trophy(players, field):
    t = get_trophy(players, field)
    if t is not None:
        print(t)


class Field:
    def __init__(self, width=16, height=9, default:int=FieldType.EMPTY):
        self.width = width
        self.height = height
        self.data = np.full((self.height, self.width), default)
        self.set_border()

    def set_border(self):
        for i in range(self.height):
            if i == 0 or i == self.height - 1:
                for j in range(self.width):
                    self.set(j, i, FieldType.WALL)
            self.set(0, i, FieldType.WALL)
            self.set(self.width-1, i, FieldType.WALL)

    def render(self, clear=True):
        if clear:
            cmd_magic.move_cursor_y(self.height)
        for i in range(self.height):
            line = ''
            for j in range(self.width):
                line += self.data[i][j].value
            print(line)

    def random_x(self):
        return random.randint(0, self.width-1)

    def random_y(self):
        return random.randint(0, self.height-1)

    def random_point(self):
        return Point(
            x=self.random_x(),
            y=self.random_y()
        )

    def random_empty_point(self):
        p = None
        while p is None or self.get(p.x, p.y) is not FieldType.EMPTY:
            p = self.random_point()
        return p

    def get_empty(self):
        p = list()
        for i in range(self.width):
            for j in range(self.height):
                if self.get(i, j) == FieldType.EMPTY:
                    p.append(Point(i, j))
        return p

    def random_empty_point2(self):
        p = self.get_empty()
        length = len(p)
        if length == 0:
            return None
        return p[random.randint(0, length-1)]

    def set_random(self, value):
        rand = self.random_point()
        self.set(rand.x, rand.y, value)
        return rand

    def set(self, x, y, value):
        self.data[y][x] = value

    def get(self, x, y):
        return self.data[y][x]

    def exists(self, x, y):
        return 0 < x < self.width and 0 < y < self.height

    def spawn_fruit(self):
        p = self.random_empty_point2()
        self.set(p.x, p.y, FieldType.FRUIT)


class RenderLoop:
    def __init__(self, field, snakes, interval=250):
        self.thread = Thread(target=self.__render_loop__, args=(interval,))
        self.field = field
        if not hasattr(snakes, '__iter__'):
            snakes = [snakes]
        if len(snakes) == 1:
            self.snake = snakes[0]
        self.snakes = snakes
        self.active = False
        self.tick_listeners = list()

    def start(self):
        self.active = True
        self.thread.start()

    def stop(self, timeout=None):
        if not self.active or not self.thread.isAlive:
            return
        self.active = False
        self.thread.join(timeout=timeout)

    def __render_loop__(self, interval):
        interval /= 1000
        while self.active and self.any_snake_alive():
            for c in self.tick_listeners:
                c()
            self.move_snakes()
            self.field.render()
            sleep(interval)

    def any_snake_alive(self):
        for snake in self.snakes:
            if snake.alive:
                return True
        return False

    def move_snakes(self):
        for snake in self.snakes:
            if snake.alive:
                snake.move()

    def add_tick_listener(self, callback):
        self.tick_listeners.append(callback)

    def remove_tick_listener(self, callback):
        self.tick_listeners.remove(callback)


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


class Snake:
    living = list()
    dead = list()

    def __init__(self, field):
        self.field = field
        self.parts = None
        self.facing = None
        self.alive = False

    def spawn(self):
        self.facing = Facing.random()
        p = self.get_spawn()
        if p is None:
            return False
        self.parts = list([p, Point(x=p.x, y=p.y), Point(x=p.x, y=p.y)])
        self.alive = True
        Snake.living.append(self)
        return True

    def die(self):
        self.alive = False
        Snake.living.remove(self)
        Snake.dead.append(self)

    def get_spawn(self):
        options = self.field.get_empty()
        random.shuffle(options)
        for o in options:
            if self.check_spawn(o):
                return o
        return None

    def check_spawn(self, point):
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

    def next_pos(self, front=None):
        if front is None:
            if len(self.parts) == 0:
                return
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

    def check_pos(self, part):
        ft = self.get_ft(part)
        return ft and self.check_ft(ft)

    @staticmethod
    def check_ft(ft):
        return ft is FieldType.EMPTY or ft is FieldType.FRUIT

    def get_ft(self, part):
        if not self.field.exists(x=part.x, y=part.y):
            return None
        return self.field.get(x=part.x, y=part.y)

    def move(self, no_apply=False):
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

    def apply_all(self):
        for part in parts:
            self.apply(part)

    def apply(self, part):
        self.field.set(part.x, part.y, FieldType.SNAKE)

    def remove_all(self):
        for part in parts:
            self.remove(part)

    def remove(self, part):
        self.field.set(part.x, part.y, FieldType.EMPTY)

    def turn_right(self):
        self.facing = self.facing.turn_right()

    def turn_left(self):
        self.facing = self.facing.turn_left()


main()
