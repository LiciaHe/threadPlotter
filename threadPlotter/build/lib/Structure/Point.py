'''
Stores a point
'''
import math
class NonNumericalError(Exception):

    def __init__(self, *args):
        if args:
            self.message=args[0]
        else:
            self.message=""
    def __str__(self):
        return "one of the location is not numerical:x and y\n"+str(self.message)
class Point:
    def __init__(self,x,y):
        self.pt=[x,y]
        if not self.isNumerical(x) or not self.isNumerical(y):
            raise NonNumericalError(self.pt)
        # print(x,y)
    def __str__(self):
        precision=2
        return str(round(self.pt[0],precision)) + "," + str(round(self.pt[1],precision))

    def copy(self):
        return Point(self.x(), self.y())
    def toList(self):
        '''
        return a clone of the pt list
        :return:
        '''
        return [self.pt[0],self.pt[1]]

    def isNumerical(self,val):
        return type(val)==int or type(val)==float
    def x(self):
        return self.pt[0]
    def y(self):
        return self.pt[1]
    def roundPt(self,digit=2):
        # print(self.pt)
        self.pt[0]=round(self.pt[0],digit)
        self.pt[1]=round(self.pt[1],digit)
        return self.pt
    def rotate(self,angle,inPlace=False):
        rad = math.radians(angle)
        c = math.cos(rad)
        s = math.sin(rad)
        x_p = self.pt[0] * c - self.pt[1] * s, 3
        y_p = self.pt[0] * s + self.pt[1] * c, 3
        if inPlace:
            self.pt=[x_p,y_p]
        return [x_p,y_p]

    def rotateAroundPoint(self,origin,angleDegree,inPlace=False):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        angleRad = math.radians(angleDegree)
        ox, oy = origin
        px, py = self.pt

        qx = ox + math.cos(angleRad) * (px - ox) - math.sin(angleRad) * (py - oy)
        qy = oy + math.sin(angleRad) * (px - ox) + math.cos(angleRad) * (py - oy)
        if inPlace:
            self.pt=[qx, qy]
        return [qx, qy]

    def scalePoints(self, scaleFactor,inPlace=False):
        '''
        ASSUME SCALING FROM CENTER
        :param points:
        :param scaleFactor:
        :return:
        '''
        scaled=[xy*scaleFactor for xy in self.pt]
        if inPlace:
            self.pt=scaled
        return scaled

    def scalePointAccordingToCenter(self, center, scaleX,scaleY,inPlace=False):
        scalePoints = [self.pt[0]*scaleX,self.pt[1]*scaleY]
        translateX = (1 - scaleX) * center[0]
        translateY = (1 - scaleY) * center[1]
        scaled=[scalePoints[0] + translateX, scalePoints[1] + translateY]
        if inPlace:
            self.pt=scaled
        return scaled
    def roughEquals(self,pt2):
        return str(self)==str(pt2)
    def translate(self,tx,ty,inplace=False):
        nPT=[self.pt[0]+tx,self.pt[1]+ty]
        if inplace:
            self.pt=nPT
        return nPT

