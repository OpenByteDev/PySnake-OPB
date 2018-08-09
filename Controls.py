from Key import Key


class Controls:
    def __init__(self, right: Key, left: Key, up: Key, down: Key):
        self.right = right
        self.left = left
        self.up = up
        self.down = down


controls = [
    Controls(
        left=Key.LEFT,
        right=Key.RIGHT,
        up=Key.UP,
        down=Key.DOWN
    ), Controls(
        left=Key.A,
        right=Key.D,
        up=Key.W,
        down=Key.S
    )]
