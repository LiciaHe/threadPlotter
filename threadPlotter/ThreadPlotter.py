'''
threadPlotter is a class that contains all the basic functions for generating a plotter-based punch needle embroidery piece.
One project is associated with one design, and can output to svgs and python files (for Axidraw)
'''

from threadPlotter.DirectAuthoringGenerator import DirectAuthoringGenerator as DirectAuthoringGenerator
import threadPlotter.Utils.basic as UB
import threadPlotter.Utils.shapeEditing as SHAPE
import threadPlotter.PunchNeedle.threadColorManagement as TM
import json

class ThreadPlotter(DirectAuthoringGenerator):

    def initSpeedAndDepthMap(self):
        '''
        generate linear mapping functions for the depth and speed
        :return:
        '''
        plotterSettingRange=self.currentSpec["plotterSettingRange"]
        self.depthRange=plotterSettingRange["depthPercRange"]
        self.speedRange=plotterSettingRange["speedPercRange"]
        distanceRange=plotterSettingRange["distanceRange"]
        self.distanceRange=[UB.unitConvert(d,self.unit,self.i2p) for d in distanceRange]

    def depthSpeedCalculator(self,distances):
        '''
        given distance, calculate speed and depth

        :param distance: a list of distances (in px)
        :return:
        '''
        disReq={}
        for dist in distances:
            speed=UB.linearScale(dist,self.distanceRange,self.speedRange)
            depth=UB.linearScale(dist,self.distanceRange,self.depthRange)
            disReq[dist]={"pen_pos_down":int(depth),"pen_rate_raise":int(speed)}
        return disReq
    def addTrailPoint(self,startPt,endPt,writerIdx):
        trailSetting=self.punchSetting["trail"]

    def processPointCneterCollection(self):
        #TODO
        return

    def closeFiles(self):
        print("exporting to " + self.getFullSaveLoc())
        self.initNewAxidrawWriter(additionalTag="master")
        for toolI,punchGroupCollection in enumerate(self.processedPointCenterCollection):
            for pgId,punchGroupAndSettingIdx in enumerate(punchGroupCollection):
                punchGroup=punchGroupAndSettingIdx[0]
                setting=self.punchSetting[punchGroupAndSettingIdx[1]]
                if pgId!=0:
                    prePoint=self.processedPointCenterCollection[pgId-1][0][-1]
                    firstPoint=punchGroupCollection[0]
                    self.addTrailPoints(prePoint,firstPoint,toolI)
                else:
                    self.updateOptions(setting,toolI)
                for punchCenter in punchGroup:
                    self.addDrawPt(punchCenter,toolI)
                    self.addDrawPt(punchCenter,-1)
                pathStr=SHAPE.getStraightPath(punchGroup)
                self.addPath(self.svg.g, pathStr, self.svg, self.tools[toolI])
                if hasattr(self, "toolSvgs"):
                    self.addPath(self.toolSvgs[toolI].g, pathStr, self.toolSvgs[toolI],
                                 self.tools[toolI])

    def saveFiles(self):
        DirectAuthoringGenerator.saveFiles(self)
        with open(self.getFullSaveLoc("tools.json"),'w') as outfile:
            json.dump(self.tools, outfile)
    def initThreadGroup(self,startingPathPoints=None):
        i

    def generate(self):
        '''
        sample generation
        :return:
        '''
        return
    def pickRandomThreadColors(self,ct=None):
        '''
        pick random thread colors (contains potential color mixing)
        :param ct:
        :return:
        '''
        if not ct:
            ct=self.basicSettings["toolsCt"]
        self.plainColor,self.mixedColor,self.colorList=TM.pickRandomThreadColor(ct)

    def matchColor(self,colorList):
        '''
        given a color list (list of rgb tuples), match the best thread color and assign to this threadPlotter object
        :param colorList:
        :return:
        '''
        self.plainColor,self.mixedColor,self.colorList=TM.pickThreadColor(colorList)

    def __init__(self,settings,batchName="",svg=True,toolSvg=True):
        DirectAuthoringGenerator.__init__(self,settings,batchName=batchName,svg=svg,toolSvg=toolSvg)
        #extract thread plotter specific information from the settings
        self.initSpeedAndDepthMap()
        self.segmentLength=UB.unitConvert(self.currentSpec["segmentLength"],self.unit,self.i2p)
        self.trailStitchLength=UB.unitConvert(self.currentSpec["trailStitchLength"],self.unit,self.i2p)
        self.pickRandomThreadColors()
        self.punchGroupCollection=[]
