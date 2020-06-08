from threadPlotter.Structure.Point import Point
from threadPlotter.Utils.shapeEditing import getStraightPath
class PunchPoint(Point):
    def __init__(self,x,y,visLength=1):
        Point.__init__(self,x,y)
        self.visLength=visLength
    def exportToPathStr(self):
        return getStraightPath([self.pt,[v+1 for v in self.pt]])
    
