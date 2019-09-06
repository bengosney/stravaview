class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return f"{self.x} x {self.y}"
        
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def moveBy(self, x, y):
        self._x += x
        self._y += y

        return self

    def moveTo(self, x, y):
        self._x = x
        self._y = y

        return self
