'''
Stores paths as list
Handles path formatting/exporting/manipulation
'''
import threadPlotter.Structure.Point as POINT
import threadPlotter.Utils.shapeEditing as SHAPE
import threadPlotter.Utils.clipperHelper as CH

class PathList:
    def __init__(self,starterArray=None,pathString=""):
        '''
        Each pathList should contain one Path

        :param starterArray: an array to be converted into PathList
        '''
        self.points=[]
        self.closed=False
        #parse from array
        if starterArray:
            for seg in starterArray:
                if len(seg)==4:
                    pts=self.convertCubicIntoLine(seg)
                    self.points+=pts
                elif len(seg)==2:
                    pt=POINT.Point(seg[0],seg[1])
                    self.points.append(pt)
                else:
                    print("seg",seg," is not a valid path segment")
                    raise ValueError
        #parse from string
        if len(pathString)>0:
            complexPath=SHAPE.convertPathToComplexPointWithPathParser(pathString)
            for seg in complexPath:
                if len(seg) == 4:
                    pts = self.convertCubicIntoLine(seg)
                    self.points += pts
                elif len(seg)==2:
                    pt = POINT.Point(seg[0], seg[1])
                    self.points.append(pt)
                else:
                    print(seg,"is not a valid seg. It contains paths whose lengths are not 2 or 4")
                    raise ValueError
            if "z" in pathString or "Z" in pathString:
                firstPt=self.points[0]
                pt = POINT.Point(firstPt.pt[0], firstPt.pt[1])
                self.points.append(pt)
                self.closed=True
                # print("closedPath",self.getLength(),self.exportPlainList())
        if len(self.points)>0:
            if self.points[0].roughEquals(self.points[-1]):
                self.closed=True
            self.getBBox()
    def appendPoint(self,x,y):
        pt = POINT.Point(x,y)
        self.points.append(pt)
    def appendPoints(self,pointList):
        for p in pointList:
            self.appendPoint(p[0],p[1])

    def __len__(self):
        return len(self.points)
    def copy(self):
        '''
        :return: a deep copy
        '''
        return PathList(starterArray=self.exportPlainList())
    def getPtByIdx(self,idx):
        return self.points[idx]

    def getBBox(self):
        '''
        this bbox is x1,x2,y1,y2 though
        :return:
        '''
        # print(self.points)
        bbox=SHAPE.getBbox(self.exportPlainList())
        # bbox=SHAPE.getBbox(self.getPathString())
        self.bbox=bbox
        # print(bbox)
        self.w=bbox[1]-bbox[0]
        self.h=bbox[3]-bbox[2]
        self.isHorizontal=self.w>self.h
        return self.bbox
    def getBBoxWHversion(self):
        return [self.bbox[0],self.bbox[2],self.bbox[1]-self.bbox[0],self.bbox[3]-self.bbox[2]]

        # return SHAPE.getBBoxWHversion(self.exportPlainList())
    def getLength(self):
        return len(self.points)
    def getCenter(self):
        '''
        XMIN,XMAX YMIN YMAX
        :return:
        '''
        self.getBBox()
        return [self.bbox[1] - self.bbox[0], self.bbox[3] + self.bbox[2]]
    def isSelfIntersecting(self):
        '''
        Determine if a path is self intersecting
        using https://algs4.cs.princeton.edu/91primitives/
        :return:
        '''
        ##todo
        return False
    def isClosed(self):
        return self.closed
    def withinSizeLimit(self,wh):
        '''
        return true if the width and height
        :param wh:
        :return:
        '''
        # print(self.bbox,wh, self.bbox[1]-self.bbox[0]<=wh[0],self.bbox[3]-self.bbox[2]<=wh[1])
        return self.bbox[1]-self.bbox[0]<=wh[0] and self.bbox[3]-self.bbox[2]<=wh[1]
    def withinBoundaryLimit(self,xmin,xmax,ymin,ymax):
        return self.bbox[0]>=xmin and self.bbox[1]<=xmax and self.bbox[2]>=ymin and self.bbox[3]<=ymax

    def adjustOriginToCenter(self):
        '''
        this will translate everything along the 0,0 point
        :return:
        not automatically called by itself
        '''
        # print(self.getPathString())

        center=self.getCenter()
        self.translate(center[0],center[1])
        self.getBBox()
        return center
    def adjustPathToLeftTop(self):
        leftTop=[self.bbox[0],self.bbox[2]]
        self.translate(-leftTop[0],-leftTop[1])
        self.getBBox()
    def exportPlainList(self,precision=None):
        lst=[pt.pt.copy() for pt in self.points]
        if precision:
            lst=[[round(pt[0],precision),round(pt[1],precision)] for pt in lst]
        return lst
    def convertCubicIntoLine(self,seg,segLength=5):
        segPoints=SHAPE.splitSingleCubicIntoLinesPoints(seg,segLength)
        # print("segPoint",segPoints)
        pts=[]
        for lineSeg in segPoints:
            for pt in lineSeg:
                if type(pt[0])!=int and type(pt[0])!=float:
                    print("pt is not numerical",pt,"seg",lineSeg)
                    raise ValueError
                pt_point=POINT.Point(pt[0],pt[1])
                if len(pts)>0 and pts[-1].roughEquals(pt_point):
                    continue
                pts.append(pt_point)
        return pts
    def getPathString(self):
        # print(self.points)
        p = "M" + " L".join([str(pt) for pt in self.points])
        if self.closed:
            return p + "Z"
        return p
    def translate(self,tx,ty):
        for pt in self.points:
            pt.translate(tx,ty,True)
        self.getBBox()
    def rotate(self,degree):
        for pt in self.points:
            # print(pt)
            pt.rotate(degree,True)
        self.getBBox()
    def rotateAroundPoint(self,center,degree):
        for pt in self.points:
            pt.rotateAroundPoint(center,degree,True)
        self.getBBox()
    def rotateAroundCenter(self,degree):
        center=[self.bbox[1]-self.bbox[0],self.bbox[3]-self.bbox[2]]
        self.rotateAroundPoint(center,degree)
    def scalePath(self,scaleFactor):
        for pt in self.points:
            pt.scalePointAccordingToCenter(scaleFactor, True)
        self.getBBox()
    def scalePathAccordingToCenter(self,center,scaleX,scaleY):
        for pt in self.points:
            pt.scalePointAccordingToCenter(center,scaleX,scaleY,True)
        self.getBBox()
    def offset(self,dist,jointType=None,offsetType=None):
        '''
        :param dist:
        :return:
        '''
        if not offsetType:
            offsetType = "CLOSEDPOLYGON"
            if not self.closed:
                offsetType = "OPENBUTT"
        if not jointType:
            jointType = "MITER"

        offsetList=CH.makeOffset(self.exportPlainList(),dist,offsetType=offsetType,jointType=jointType)
        if len(offsetList)>0:
            if self.closed or offsetType.upper().startswith("OPEN"):
                offsetList[0].append(offsetList[0][0].copy())
            return offsetList[0]
        return offsetList
    def exportToStr(self):
        return "<path d=\""+str(self)+"\">"
    def __str__(self):
        return SHAPE.getStraightPath(self.exportPlainList())




