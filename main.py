from Player import Player
from Snake import Snake
from Field import Field
from RenderLoop import RenderLoop
from Key import Key
from Controls import controls
import cmd_magic

from typing import Optional, List
from colorama import Style
import msvcrt
import argparse


def parse_args() -> object:
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


def get_trophy(players: List[Player], field: Field) -> Optional[str]:
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


def print_trophy(players: List[Player], field: Field) -> None:
    t = get_trophy(players, field)
    if t is not None:
        print(t)


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


main()
