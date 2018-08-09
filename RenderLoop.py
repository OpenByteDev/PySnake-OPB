from Snake import Snake
from Field import Field

from threading import Thread
from time import sleep
from typing import Union, Iterable, Optional, Callable


class RenderLoop:
    def __init__(self, field: Field, snakes: Union[Iterable[Snake], Snake], interval: int=250):
        self.thread = Thread(target=self.__render_loop__, args=(interval,))
        self.field = field
        if not hasattr(snakes, '__iter__'):
            snakes = [snakes]
        if len(snakes) == 1:
            self.snake = snakes[0]
        self.snakes = snakes
        self.active = False
        self.tick_listeners = list()

    def start(self) -> None:
        self.active = True
        self.thread.start()

    def stop(self, timeout: Optional[int]=None) -> None:
        if not self.active or not self.thread.isAlive:
            return
        self.active = False
        self.thread.join(timeout=timeout)

    def __render_loop__(self, interval: int) -> None:
        interval /= 1000
        while self.active and self.any_snake_alive():
            for c in self.tick_listeners:
                c()
            self.move_snakes()
            self.field.render()
            sleep(interval)

    def any_snake_alive(self) -> bool:
        for snake in self.snakes:
            if snake.alive:
                return True
        return False

    def move_snakes(self) -> None:
        for snake in self.snakes:
            if snake.alive:
                snake.move()

    def add_tick_listener(self, callback: Callable) -> None:
        self.tick_listeners.append(callback)

    def remove_tick_listener(self, callback: Callable) -> None:
        self.tick_listeners.remove(callback)
