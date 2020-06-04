import sys
sys.path.insert(1,"../../../")
import threadPlotter.Structure.PathList as PL
import threadPlotter.Utils.shapeEditing as SHAPE
class TransformError(Exception):
    def __init__(self, *args):
        if args:
            self.message=args[0]
        else:
            self.message=""
    def __str__(self):
        return self.message+" contains transformation. Make sure your svg has a flat structure(avoid applying transformations in groups),and all paths have no transformation."
class PunchGroup:
    '''
    contains one path
    modify path
    '''

    def __init__(self,pathInput,id):
        '''
        construct pathList
        Can only contain a path element
        :param path:
        '''
        self.id = id
        if isinstance(pathInput,list):
            #process from pathList
            self.pathList = PL.PathList(starterArray=pathInput)
        elif isinstance(pathInput,PL.PathList):
            self.pathList=pathInput
        else:
            if "transform" in pathInput.attrs:
                raise TransformError(pathInput)
            d = pathInput.attrs["d"]
            self.pathList = PL.PathList(pathString=d)
        self.originalPathList=self.pathList.copy()
        # self.adjustOriginToCenter()
    def appendPathPoints(self,xyList):
        for p in xyList:
            self.addPoint(p[0],p[1])
    def addPoint(self,x,y):
        self.pathList.appendPoint(x,y)
    def copy(self,id=None):
        if id==None:
            id=str(self.id)+"_copy"
        return PunchGroup(self.exportToPlainList(),id)
    def adjustOriginToCenter(self):
        self.originalCenter=self.pathList.adjustOriginToCenter()
    def translate(self,x,y):
        self.pathList.translate(x,y)
    def getPath(self):
        return self.pathList.getPathString()
    def getBBox(self):
        '''
        return and update this bbox
        x,y,w,h
        :return:
        '''
        self.bbox=self.pathList.getBBoxWHversion()
        return self.bbox
    def getLoc(self,xKey,yKey):
        center = self.getCenter()
        xPoint={
            "LEFT":self.bbox[0],
            "RIGHT":self.bbox[0]+self.bbox[2],
            "CENTER":center[0]
        }
        yPoint={
            "TOP":self.bbox[1],
            "BOTTOM":self.bbox[1]+self.bbox[3],
            "CENTER":center[1]
        }
        return [xPoint[xKey],yPoint[yKey]]
    def isClosed(self):
        return self.pathList.closed
    def getCenter(self):
        self.getBBox()
        return [self.bbox[0] + self.bbox[2] / 2, self.bbox[1] + self.bbox[3]]
    def exportToStr(self):
        d=SHAPE.getStraightPath(self.pathList.exportPlainList())
        return "<path d=\""+d+"\">"
    def scaleAccordingToCenter(self,center,scaleX,scaleY):
        self.pathList.scalePathAccordingToCenter(center,scaleX,scaleY)
    def offset(self,dist,offsetType,jointType):
        return self.pathList.offset(dist,offsetType,jointType)
    def rotate(self,center,degree):
        self.pathList.rotateAroundPoint(center,degree)
    def restore(self):
        self.pathList=self.originalPathList.copy()
        self.getBBox()
    def exportToPlainList(self,precision=2):
        return self.pathList.exportPlainList(precision=precision)
    def __len__(self):
        return len(self.pathList)
    def getFirstPt(self):
        if len(self.pathList)==0:
            return None
        return self.pathList.getPtByIdx(0)
    def getLastPt(self):
        if len(self.pathList)==0:
            return None
        return self.pathList.getPtByIdx(-1)

    def __str__(self):
        return self.exportToStr()