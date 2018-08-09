import subprocess as sp


def init():
    sp.call('', shell=True)


def clear_line():
    print(chr(27) + "[1K")


def clear_screen():
    print(chr(27) + "[2J")


def save_cursor():
    print(chr(27) + "[s")


def restore_cursor():
    print(chr(27) + "[u")


def move_cursor_x(val):
    if val > 0:
        print(chr(27) + "[%dC" % val)
    elif val < 0:
        print(chr(27) + "[%dD" % abs(val))


def move_cursor_y(val):
    if val == 0:
        return
    val += 1
    if val > 0:
        print(chr(27) + "[%dA" % val)
    elif val < 0:
        print(chr(27) + "[%dB" % abs(val))

