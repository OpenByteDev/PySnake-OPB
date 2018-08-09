class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def shift(self, x, y):
        self.x += x
        self.y += y
        return self

    def clone(self):
        return Point(x=self.x, y=self.y)

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])
