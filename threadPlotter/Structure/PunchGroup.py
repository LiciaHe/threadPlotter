
from threadPlotter.Structure.PathList import PathList

from threadPlotter.Utils.shapeEditing import pressIntoABox

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

    def __init__(self,pathInput,id,segmentLengt):
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
        self.originalPathList=self.exportPlainList().copy()

    def exportToPunchNeedleReadyPoints(self,segmentLength,boundaryRect,addStartingTrail=False,addEndingTrail=False,minDistance=2):
        '''
        segment the punch groups by the segment length
        Tasks:
        1. for each segment in the
        :return: a list of PunchPoint objects

        :param segmentLength:
        :param boundaryRect: XMIN,YMIN,XMAX,YMAX
        :param addStartingTrail:
        :param addEndingTrail:
        :param minDistance:
        :return:
        '''
        plainPoints=self.exportPlainList(precision=2)
        SHAPE.pres

    def restore(self):
        self.points=self.originalPathList.copy()
        self.getBBox()
