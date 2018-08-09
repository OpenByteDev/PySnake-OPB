import subprocess as sp


initialized = False


def init() -> None:
    sp.call('', shell=True)
    global initialized
    initialized = True


def clear_line() -> None:
    print(chr(27) + "[1K")


def clear_screen() -> None:
    print(chr(27) + "[2J")


def save_cursor() -> None:
    print(chr(27) + "[s")


def restore_cursor() -> None:
    print(chr(27) + "[u")


def move_cursor_x(val: int) -> None:
    if val > 0:
        print(chr(27) + "[%dC" % val)
    elif val < 0:
        print(chr(27) + "[%dD" % abs(val))


def move_cursor_y(val: int) -> None:
    if val == 0:
        return
    val += 1
    if val > 0:
        print(chr(27) + "[%dA" % val)
    elif val < 0:
        print(chr(27) + "[%dB" % abs(val))
