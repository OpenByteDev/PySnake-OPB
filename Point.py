class Point:
    def __init__(self, x: int=0, y: int=0):
        self.x = x
        self.y = y

    def shift(self, x: int, y: int):
        self.x += x
        self.y += y
        return self

    def clone(self):
        return Point(x=self.x, y=self.y)

    def __repr__(self) -> str:
        return ''.join(['Point(', str(self.x), ',', str(self.y), ')'])
