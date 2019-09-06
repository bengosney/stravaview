import polyline
from point import Point

LAT_INDEX = 0
LNG_INDEX = 1

class Route:
    def __init__(self, route):
        rawPoints = polyline.decode(route)

        self._points = [Point(p[LAT_INDEX], p[LNG_INDEX]) for p in rawPoints]
        self._setChanged()

    def __str__(self):
        return "\n".join([str(p) for p in self.points])

    @property
    def points(self):
        return self._points
        
    @property
    def x(self):
        return [p.x for p in self.points]

    @property
    def y(self):
        return [p.y for p in self.points]

    def applyMod(self, x, y):
        self._setChanged()
        for p in self.points:
            p.moveBy(x, y)

    def _setChanged(self):
        self._maxX = None
        self._maxY = None
        self._minX = None
        self._minY = None

    @property
    def maxX(self):
        if self._maxX is None:
            self._maxX = max([p.x for p in self.points])            

        return self._maxX

    @property
    def maxY(self):
        if self._maxY is None:
            self._maxY = max([p.y for p in self.points])            

        return self._maxY

    @property
    def minX(self):
        if self._minX is None:
            self._minX = min([p.x for p in self.points])            

        return self._minX

    @property
    def minY(self):
        if self._minY is None:
            self._minY = min([p.y for p in self.points])            

        return self._minY
    
            
    def normalize(self):
        minX = min(self.x)
        if minX < 0:
            modX = abs(minX)
        else:
            modX = -minX
                
        minY = min(self.y)
        if minY < 0:
            modY = abs(minY)
        else:
            modY = -minY

        self.applyMod(modX, modY)

    def _scaleRange(OldValue, OldMin, OldMax, NewMin, NewMax):
        OldRange = (OldMax - OldMin)  
        NewRange = (NewMax - NewMin)

        return (((OldValue - OldMin) * NewRange) / OldRange) + NewMin


    def scaleWithin(self, width, height):
        minX = min(self.x)
        maxX = max(self.x)

        minY = min(self.y)
        maxY = max(self.y)
        
        fw = width / maxX
        fh = height / maxY
        f = min(fw, fh)
        for p in self.points:
            p.moveTo(p.x * f, p.y * f)
            

    def scaleToMaxY(self, scaleTo):
        pass
                
