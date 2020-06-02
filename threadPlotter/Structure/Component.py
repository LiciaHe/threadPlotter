import sys
sys.path.insert(1,"../../../")
import Utils.PathList as PL
from SvgManipulation import shapeMaker as SHAPE
from SvgManipulation import pathUtils as PU
from Utils.Element import Element
from bs4 import BeautifulSoup
from bs4 import element as bs4element

from LaserCutter.LayerArt.Helper.Errors import *
class CantParseElementError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = ""

    def __str__(self):
        return self.message + "\nCannot process this svg tag. The accepted list of tags is:[g,path,circle,rect,line]"
class Component:
    '''
    Each component is one group of variations
    Contains multiple key elements (paths)
    '''
    def makeElementPathFromPathPoint(self,pathPoint,elemId):
        path = '<path d="' + SHAPE.getStraightPath(pathPoint) + '">'
        return Element(BeautifulSoup(path, "html.parser").path, elemId)
    def processOneTag(self,tag):
        # print(tag)
        '''
        parse info into component and element
        :param tag:
        :return:
        '''
        id=str(self.childCounter)
        # convert every element into rectangle
        if tag.name =="g":
            # process the following paths
            # tagId=str(sum(self.isComponent))
            comp=Component(tag,id)
            toAppend=comp
            self.isComponent.append(1)
        elif  tag.name == "path":
            # start element
            toAppend=Element(tag,id)
        elif  tag.name == "circle":
        # process
            cx=float(tag.attrs["cx"])
            cy=float(tag.attrs["cy"])
            r=float(tag.attrs["r"])
            toAppend = self.makeElementPathFromPathPoint(SHAPE.makeCirclePoints(cx,cy,r),id)
        elif  tag.name == "rect":
            #curved rectangle not supported yet
            x = tag.attrs["x"]
            y = tag.attrs["y"]
            if "w" in tag.attrs:
                w = tag.attrs["w"]
                h = tag.attrs["h"]
            else:
                w = tag.attrs["width"]
                h = tag.attrs["height"]
            toAppend = self.makeElementPathFromPathPoint(SHAPE.makeRectPoints(float(x),float(y),float(w),float(h)),id)
        # process rect
        elif  tag.name == "line":
            # process line
            x1 = tag.attrs["x1"]
            x2 = tag.attrs["x2"]
            y1 = tag.attrs["y1"]
            y2 = tag.attrs["y2"]
            toAppend = self.makeElementPathFromPathPoint([float(x1),float(y1),float(x2),float(y2)],id)
        elif  tag.name=="polygon":
            points=[[float(xy) for xy in pt.split(",")] for pt in tag.attrs["points"].strip().split(" ")]
            points.append(points[0].copy())
            toAppend = self.makeElementPathFromPathPoint(points,id)
        else:
            print(tag,tag.name)
            raise CantParseElementError
        self.childCounter+=1
        self.childList.append(toAppend)
        return toAppend

    def __init__(self,groupInput,id):
        self.id=id
        self.childList=[] #can store element or store processOneTag
        self.isComponent = []  # for each child, store 1 if it's a component instead of an element
        # print(id)
        self.childCounter = 0
        if groupInput!=None:
            if isinstance(groupInput,list):
                #init from pathList
                self.childCounter=1
                self.isComponent.append(0)
                #make an element
                self.childList.append(Element(groupInput,str(0)))
            elif groupInput.name in ["path","circle","rect","line","polygon"]:
                #init from
                self.processOneTag(groupInput)
            elif isinstance(groupInput,bs4element.Tag):
                for i,tag in enumerate(groupInput):
                    if not tag.name:
                        continue
                    self.processOneTag(tag)
            else:
                raise CantParseElementError()
        #create empty element
        self.getBBox()

    def stretchTo(self,idealWidth,idealHeight):
        scaleX=idealWidth/self.bbox[2]
        scaleY=idealHeight/self.bbox[3]
        self.scaleAccordingToCenter(self.getCenter(),scaleX,scaleY,unit="px")
        self.getBBox()

    def appendToChild(self,component):
        self.childList.append(component)
        self.childCounter+=1
        self.getBBox()
    def getBBox(self):
        '''
        return the x,y,w,h of all children
        will revert the previous list
        :return:
        '''

        self.center=[]
        preBox=None
        for child in self.childList:
            bbox=child.getBBox()
            if preBox!=None:
                preBox=PU.mergeBoundingBox(preBox,bbox)
            else:
                preBox=bbox
        self.bbox=preBox
        return self.bbox
    def getCenter(self):
        '''
        get x, y
        :return:
        '''
        self.getBBox()
        return [self.bbox[0]+self.bbox[2]/2,self.bbox[1]+self.bbox[3]/2]
    def translate(self,x,y):
        '''
        for every thing underneath here, translate by x and y
        :param x:
        :param y:
        :return:
        '''
        for child in self.childList:
            child.translate(x,y)
        self.getBBox()
    ##todo: make original translation. Need to ensure the original location point is set to the correct point
    def exportToStr(self):
        start="<g>"
        end="</g>"
        for child in self.childList:
            # print(child)
            start+=child.exportToStr()
        return start+end
    def getLoc(self,xKey,yKey):
        # if parseNone and xKey==None:
        #
        center = self.getCenter()
        xPoint = {
            "LEFT": self.bbox[0],
            "RIGHT": self.bbox[0] + self.bbox[2],
            "CENTER": center[0]
        }
        yPoint = {
            "TOP": self.bbox[1],
            "BOTTOM": self.bbox[1] + self.bbox[3],
            "CENTER": center[1]
        }
        # print(xKey,yKey)
        return [xPoint[xKey], yPoint[yKey]]
    def scaleAccordingToCenter(self,center,scaleX,scaleY=None,unit="px"):

        if not scaleY:
            scaleY=scaleX
        xKey=center[0]
        yKey=center[1]
        if isinstance(xKey,str):
            center=self.getLoc(xKey,yKey)
        elif isinstance(xKey,float) or isinstance(xKey,int):
            center=[PU.unitConvert(xKey,unit),PU.unitConvert(yKey,unit)]
        else:
            raise InvalidInputParameterError('Invalid x y keys'+str(xKey)+","+str(yKey)+"\n")
        for child in self.childList:
            child.scaleAccordingToCenter(center,scaleX,scaleY)
    def offset(self,dist,offsetType,jointType):
        '''

        :param dist:
        :return: a list of pathPoints (as list)
        '''
        results=[]
        for child in self.childList:
            newPath=child.offset(dist,offsetType,jointType)
            if len(newPath)>0 and len(newPath[0])>0:
                results.append(newPath)
        return results
    def rotate(self,center,degree,unit="px"):
        '''
        :param center: x, y in pixels
        :param degree:
        :return:
        '''
        xKey = center[0]
        yKey = center[1]

        if isinstance(xKey, str):
            center = self.getLoc(xKey, yKey)
        elif isinstance(xKey, float) or isinstance(xKey, int):
            center = [PU.unitConvert(xKey, unit), PU.unitConvert(yKey, unit)]
        else:
            raise InvalidInputParameterError('Invalid x y keys' + str(xKey) + "," + str(yKey) + "\n")
        # print(center, degree)
        for elem in self.childList:
            elem.rotate(center,degree)
    def restore(self):
        for c in self.childList:
            c.restore()
        self.getBBox()
    def split(self):
        '''
        separate the child list into individual components
        :return:
        '''
        newComps=[]
        for i,child in enumerate(self.childList):
            newComp=Component(groupInput=None,id=self.id+"_"+str(i))
            newComp.appendToChild(child)
            newComps.append(newComp)
        return newComps
    def exportToPlainList(self):
        '''
        for each child within this component, export a
        list of points[]
        If the child component is also a component, this method does not flatten it
        :return:
        '''
        plainList=[]
        for child in self.childList:
            plainList.append(child.exportToPlainList())
        return plainList
    def exportToFlattenList(self):
        '''
        only contains pathList, without hierarchy
        :return:
        '''
        flattenList=[]
        for child in self.childList:
            if isinstance(child,Component):
                # print("flatten")
                flattenList+=child.exportToFlattenList()
            else:
                flattenList+=child.exportToPlainList()
        return flattenList
    def isClosed(self):
        '''
        everything in this component needs to be closed
        :return:
        '''
        return all([c.isClosed() for c in self.childList])
    def copy(self,id=None):
        '''
        :return:  a copy of this
        '''
        if id==None:
            id=str(self.id)+"_copy"
        newComp=Component(None,id)
        for c in self.childList:
            newC=c.copy()
            newComp.appendToChild(newC)
        return newComp






    def __str__(self):
        return self.exportToStr()









