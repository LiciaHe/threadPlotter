
from threadPlotter.Structure.PathList import PathList
import threadPlotter.Utils.shapeEditing as SHAPE
class TransformError(Exception):
    def __init__(self, *args):
        if args:
            self.message=args[0]
        else:
            self.message=""
    def __str__(self):
        return self.message+" contains transformation. Make sure your svg has a flat structure(avoid applying transformations in groups),and all paths have no transformation."
class InvalidPathPointInput(Exception):
    def __init__(self, *args):
        if args:
            self.message=args[0]
        else:
            self.message=""
    def __str__(self):
        return self.message+" is not a valid list, str, PathList object, or beautiful soup object."
class PunchGroup(PathList):
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
            PathList.__init__(self,starterArray=pathInput)
        elif isinstance(pathInput,PathList):
            PathList.__init__(self, starterArray=pathInput.exportPlainList())
        elif isinstance(pathInput,str):
            PathList.__init__(self, pathString=pathInput)
        else:
            try:
                if "transform" in pathInput.attrs:
                    raise TransformError(pathInput)
                d = pathInput.attrs["d"]
                PathList.__init__(self,pathString=d)
            except:
                raise InvalidPathPointInput(pathInput)
        self.originalPathList=self.exportToPlainList().copy()


    def exportToPunchNeedleReadyPoints(self,segmentLength,boundaryRect):
        '''
        segment the punch groups by the segment length
        :return: a list of
        '''
        #todo

    def copy(self,id=None):
        if id==None:
            id=str(self.id)+"_copy"
        return PunchGroup(self.exportToPlainList(),id)

    def getPath(self):
        return self.pathList.getPathString()



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