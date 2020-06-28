
from threadPlotter.Structure.PathList import PathList

from threadPlotter.Utils.shapeEditing import pressIntoABox
from threadPlotter.PunchNeedle import embroideryCalculation as EC
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

    def __init__(self,pathInput,id,toolId,skipSegment):
        '''
        construct pathList
        Can only contain a path element
        :param path:
        '''
        self.id = id
        self.toolId=toolId
        self.skipSegment=skipSegment
        if pathInput==None:
            PathList.__init__(self)
        elif isinstance(pathInput,list):
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
        if self.skipSegment:
            return plainPoints
        if addStartingTrail:
            plainPoints=[[0,0]]+plainPoints
        if addEndingTrail:
            plainPoints.append([0,0])
        pressIntoABox(plainPoints,boundaryRect[0],boundaryRect[1],boundaryRect[2],boundaryRect[3])

        dotList=EC.makeConnectedDot(plainPoints,segmentLength,minDistance)
        return dotList

    def exportTrailToAnotherPunchGroup(self,punchGroup2,trailLength,minDistance=2):
        '''
        return a list of trail point centers that connects to pucnh group 2
        :param punchGroup2:
        :return:
        '''
        try:
            thisPoint = self.points[-1].toList()
            nextPt=punchGroup2.getPtByIdx(0).toList()
        except IndexError:
            return []
        dotList = EC.makeConnectedDot([thisPoint,nextPt], trailLength, minDistance)
        return dotList


    def restore(self):
        self.points=self.originalPathList.copy()
        self.getBBox()
