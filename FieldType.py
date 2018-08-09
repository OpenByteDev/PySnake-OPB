from colorama import Fore, Back, Style
from enum import Enum


class FieldType(Enum):
    EMPTY = '  '
    SNAKE = Back.WHITE + '  ' + Back.RESET
    FRUIT = Back.RED + '  ' + Back.RESET
    WALL = Back.LIGHTBLACK_EX + '  ' + Back.RESET
