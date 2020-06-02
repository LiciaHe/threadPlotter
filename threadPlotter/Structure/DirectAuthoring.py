'''
Only produce axidraw Files
'''
import math
import sys
sys.path.insert(1,"../")
import random,datetime,os
import Utils.basic as UB
import SvgManipulation.pathUtils as PU
from ArtGenerator.MainGenerator import MainGenerator
import SvgManipulation.Svg as SVG
import SvgManipulation.shapeMaker as SHAPE
class DirectAuthoring(MainGenerator):
    def writeEmptyUpdate(self,writerIdx):
        self.axidrawWriters[writerIdx].write("ad.penup()\n")
        self.axidrawWriters[writerIdx].write("ad.move(0,0)\n")
    def updateOptions(self,req,writerIdx):
        '''
        update setting manually
        assume axidraws are initiated
        :param req:
        :return:
        '''

        for key in req:
            self.axidrawWriters[writerIdx].write("ad.options." + key + "=" + str(req[key]) + "\n")
        self.axidrawWriters[writerIdx].write( "ad.update()\n")
    def addPenUp(self,writerIdx):
        self.axidrawWriters[writerIdx].write("ad.penup()\n")
    def addPenDown(self,writerIdx):
        self.axidrawWriters[writerIdx].write("ad.pendown()\n")
    def addDrawPt(self,dotCenter,writerIdx,withMargin=True):
        '''
        use only up and down
        :param dotCenter:
        :param toolIdx:
        :return:
        '''
        self.addMoveTo(dotCenter, writerIdx, withMargin=withMargin)
        self.axidrawWriters[writerIdx].write("ad.pendown()\n")
        self.axidrawWriters[writerIdx].write("ad.penup()\n")
    def calculateAxidrawPosition(self,pt,writerIdx,withMargin=True):
        dotPathInInches = PU.ptToInchStrWithTranslate(pt, self.i2p, self.marginInch["l"], self.marginInch["t"])
        if not withMargin:
            dotPathInInches=PU.ptToInchStr(pt,self.i2p,precision=2)
        return dotPathInInches
    def addMoveTo(self,dotCenter, writerIdx, withMargin=True):
        dotPathInInches=self.calculateAxidrawPosition(dotCenter,writerIdx,withMargin=withMargin)
        self.axidrawWriters[writerIdx].write("ad.moveto(" + dotPathInInches[0] + "," + dotPathInInches[1] + ")\n")
    def addLineTo(self,pt,writerIdx,withMargin=True):
        dotPathInInches = self.calculateAxidrawPosition(pt, writerIdx, withMargin=withMargin)
        self.axidrawWriters[writerIdx].write("ad.lineto(" + dotPathInInches[0] + "," + dotPathInInches[1] + ")\n")
    def addDrawingAndRefill(self,pathPoints,writerIdx,breakLength,toolPanIdx=-1):
        '''
        Drawing and refilling at the same time
        :param pathPoints:
        :param writerIdx:
        :param breakLength:
        :param toolPanIdx:
        :param stir:
        :return:
        '''
        currentLength=0
        for i,pt in enumerate(pathPoints):
            if i==0:
                self.addMoveTo(pt,writerIdx)
            else:
                currentLength+=PU.calculateDistBetweenPoints(pathPoints[i-1],pt)
                if currentLength>breakLength:
                    self.addInkRefillInstruction(writerIdx,toolPanIdx)
                    self.addMoveTo(pathPoints[i-1],writerIdx)
                    self.addLineTo(pt,writerIdx)
                    currentLength=0
                self.addLineTo(pt,writerIdx)
        return currentLength
    def addDrawing(self,pathPoints,writerIdx):
        for i, pt in enumerate(pathPoints):
            if i == 0:
                self.addMoveTo(pt, writerIdx)
            else:
                self.addLineTo(pt,writerIdx)



    def addInkRefillInstruction(self,writerIdx,toolIdx=-1):
        '''
        return to normal setting after the re ink
        :param writerIdx:
        :param toolIdx:
        :return:
        '''
        if toolIdx==-1:
            toolIdx=random.randint(0,self.toolsCt-1)
        toolLoc=[self.toolX,self.getToolPanY(toolIdx)]
        self.updateOptions(self.basicSettings["toolsSetting"],writerIdx)
        self.writeEmptyUpdate(writerIdx)
        if self.stir:
            # print(toolIdx)
            stirPath=self.toolStir[toolIdx]
            self.addMoveTo(stirPath[0], writerIdx, withMargin=False)
            for pt in stirPath[1:]:
                self.addLineTo(pt, writerIdx, withMargin=False)
        else:
            self.addDrawPt(toolLoc, writerIdx,withMargin=False)
        self.updateOptions(self.basicSettings["normalSetting"],writerIdx)
    def addComment(self,comment,toolIdx):
        self.axidraws[toolIdx].write("##"+comment+"\n")
    def initNewAxidrawWriter(self,additionalTag=""):
        axidrawHeader =[
            "'''\n auto-generated axidraw code \n'''\nfrom pyaxidraw import axidraw\nimport time\nad =axidraw.AxiDraw()\nad.interactive()\nad.connect()\n",
            "ad.options.model=2\n",
            "ad.options.pen_rate_lower=80\n",
            "ad.options.pen_rate_upper=80\n"
        ]
        axidrawHeaderEnd=[
            "ad.penup()",
            "ad.moveto(0, 0)",
            "ad.penup()",
            "ad.pendown()\n"
        ]
        currentName=self.getFullSaveLoc(additionalTag=additionalTag+"_"+str(len(self.axidrawWriters)))

        axidrawWriter=open(currentName+".py","w")
        self.axidrawWriters.append(axidrawWriter)
        axidrawWriter.write("\n".join(axidrawHeader) + "\n")
        self.updateOptions(self.normalSetting,len(self.axidrawWriters)-1)
        axidrawWriter.write("\n".join(axidrawHeaderEnd))
        return len(self.axidrawWriters)-1
    def getToolPanY(self, idx):
        if idx==-1:
            idx=self.getRandomToolId()
        return self.toolPanYs[idx]
    def appendToAxidrawCollection(self,pathPoints,toolIdx=-1):
        '''
        adding a path into the path collection
        :param pathPoints:
        :param toolIdx:
        :return:
        '''
        if not hasattr(self,"axidrawPathCollection"):
            self.axidrawPathCollection=[]
            for i in range(len(self.tools)):
                self.axidrawPathCollection.append([])
        if toolIdx<0:
            toolIdx=self.getRandomToolId()

        self.axidrawPathCollection[toolIdx].append(pathPoints)

    def initToolPanSetting(self):
        '''
        fixed the toolpan towards the end
        :return:
        '''

        self.toolPanAttr = []
        self.r = PU.unitConvert(0.8, "inch", 96)

        self.toolX = PU.unitConvert(15,"inch",96) + self.r
        self.toolY = PU.unitConvert(1,"inch",96)
        self.toolPanDist = self.basicSettings["toolPanDist"] if "toolPanDist" in self.basicSettings else 20
        self.toolInnerR=self.r*0.6
        self.toolStir=[]
        self.toolPanYs=[]
        for i in range(self.toolsCt):

            y = (self.toolY + self.r) + (self.r * 2 + self.toolPanDist) * i
            self.toolPanYs.append(y)
            poly=SHAPE.makeUniformPolygon(self.toolX, y, self.toolInnerR, 10)
            self.toolStir.append(poly)
    def addTimeOut(self,breakTimeInSec):
        self.axidrawWriters[-1].write("time.sleep("+str(breakTimeInSec)+")\n")
    def closeFiles(self,checkBoundary=True):
        if hasattr(self,"axidrawPathCollection"):
            print("export to master")
            #perform all appending
            #master  writer
            self.initNewAxidrawWriter(additionalTag="master")
            currentLength=0
            if "betweenToolBreakMin" in self.basicSettings:
                self.betweenBreakSec=self.basicSettings["betweenToolBreakMin"]*50
            for i,coll in enumerate(self.axidrawPathCollection):
                for pathPoints in coll:
                    if checkBoundary:
                        minX, maxX, minY, maxY=PU.getBoundaryBoxPtsVersion(pathPoints)
                        if minX>self.wh_m[0] or minY>self.wh_m[1]:
                            continue
                        PU.pressIntoABox(pathPoints,0,0,self.wh_m[0],self.wh_m[1])
                    if self.initToolPan:
                        self.addInkRefillInstruction(i, toolIdx=0)
                        currentLength+=self.addDrawingAndRefill(pathPoints, i, self.breakLength, toolPanIdx=0)
                        self.addDrawingAndRefill(pathPoints, -1, self.breakLength, toolPanIdx=i)
                        if currentLength > self.breakLength:
                            self.addInkRefillInstruction(i, toolIdx=0)
                            self.addInkRefillInstruction(-1, toolIdx=i)
                            currentLength = 0
                    else:
                        self.addDrawing(pathPoints,i)
                        self.addDrawing(pathPoints,-1)
                    self.addPath(self.svg.g, SHAPE.getStraightPath(pathPoints), self.svg, self.tools[i])
                    if hasattr(self, "toolSvgs"):
                        self.addPath(self.toolSvgs[i].g, SHAPE.getStraightPath(pathPoints),self.toolSvgs[i], self.tools[i])
                self.addMoveTo([0, 0], i, withMargin=False)
                if hasattr(self,"betweenBreakSec"):
                    self.addTimeOut(self.betweenBreakSec)

        for axidrawWriter in self.axidrawWriters:
            axidrawWriter.close()
    def saveFiles(self):
        self.closeFiles()
        if hasattr(self,"svg"):
            self.saveSvg(self.svg)
        if hasattr(self,"toolSvgs"):
            for i,s in enumerate(self.toolSvgs):
                self.saveSvg(s,str(i))

    def __init__(self,settings,initToolPan=True,svg=True,toolSvg=True,batchName=""):
        self.initToolPan=initToolPan
        # name, currentSetting, basicSettings
        MainGenerator.__init__(self,settings=settings,batchName=batchName)

        self.initToolPan=initToolPan
        self.strokeWidth = self.basicSettings["strokeWidth"] if "strokeWidth" in self.basicSettings else 5
        if initToolPan:
            self.initToolPanSetting()
            self.stir=self.basicSettings["stir"] if "stir" in self.basicSettings else False
            self.breakLength = self.basicSettings["refillLength"] if "refillLength" in self.basicSettings else 250
        if svg:
            self.svg, self.wh, self.wh_m, self.boundaryRect, self.margins = SVG.makeBasicSvgWithFoundations(
                self.basicSettings)
            self.generateRandomTools()
            if toolSvg:
                self.toolSvgs=[]
                for i in range(len(self.tools)):
                    svg, wh, whm, br, m = SVG.makeBasicSvgWithFoundations(
                        self.basicSettings)
                    self.toolSvgs.append(svg)
        for i in range(len(self.tools)):
            self.initNewAxidrawWriter()



