'''
threadPlotter is a class that contains all the basic functions for generating a plotter-based punch needle embroidery piece.
One project is associated with one design, and can output to svgs and python files (for Axidraw)
'''

from threadPlotter.DirectAuthoringGenerator import DirectAuthoringGenerator as DirectAuthoringGenerator
from threadPlotter.TP_utils.shapeEditing import convertListToDotStr

from threadPlotter.TP_punchneedle import threadColorManagement as TCM
from threadPlotter.TP_utils import basic as UB
from threadPlotter.TP_structure.PunchGroup import PunchGroup
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

    def depthSpeedCalculator_batch(self,distance):
        storage={}
        for dist in distance:
            storage[dist]=self.depthSpeedCalculator(dist)
        return storage
    def depthSpeedCalculator(self,dist):
        '''
        given distance, calculate speed and depth

        :param distance: a list of distances (in px)
        :return:
        '''
        speed = UB.linearScale(dist, self.distanceRange, self.speedRange)
        depth = UB.linearScale(dist, self.distanceRange, self.depthRange)
        return {"pen_pos_down": int(depth), "pen_rate_raise": int(speed)}



    def closeFiles(self):
        '''
        Assuming all information has been stored in the list:
        self.punchGroupCollection
        for each punch group, process the information contained (segment into center points) and export to svg and python.
        :return:
        '''
        lastPgId=len(self.punchGroupCollection)-1
        boundaryBox=[0,0,self.wh_m[0],self.wh_m[1]]

        for pgi,punchGroup in enumerate(self.punchGroupCollection):
            toolId=punchGroup.toolId
            dotList=punchGroup.exportToPunchNeedleReadyPoints(self.segmentLength,boundaryBox)
            if len(dotList)<1:
                continue
            trailList=[]
            if pgi!=lastPgId:
                trailList=punchGroup.exportTrailToAnotherPunchGroup(
                    self.punchGroupCollection[pgi+1],
                    self.trailStitchLength
                )
            self.updateOptions(self.stitchSetting,toolId)
            for pt in dotList:
                self.addDrawPt(pt,toolId)
            self.updateOptions(self.trailStitchSetting,toolId)
            for trailPt in trailList:
                self.addDrawPt(trailPt,toolId)

            pathStrs = convertListToDotStr(dotList+trailList)
            for ps in pathStrs:
                self.addPath(self.svg.g, ps, self.svg, self.tools[toolId])
                if hasattr(self, "toolSvgs"):
                    self.addPath(self.toolSvgs[toolId].g, ps, self.toolSvgs[toolId],
                                 self.tools[toolId])


    def saveFiles(self):
        print("exporting to " + self.getFullSaveLoc())
        self.closeFiles()
        DirectAuthoringGenerator.saveFiles(self)
        #export thread matching guide
        self.generateColorPlan()

    def initPunchGroup(self,toolId,startingPathPoints=None,skipSegment=False):
        '''
        make a thread group, append to storage.
        :param startingPathPoints:
        :return: index of this threadGroup
        '''
        pgI=len(self.punchGroupCollection)
        self.punchGroupCollection.append(
            PunchGroup(startingPathPoints,pgI,toolId,skipSegment)
        )
        return pgI
    def generateColorPlan(self):
        '''
        export the color plan into svg and json files
        :return:
        '''

        svg, width_height, wh_m, boundaryRect, margins= svg.makeBasicSvgWithFoundations({"paperWidth":5, "paperHeight": len(self.colorList) * 2, "inchToPx":96, "margins":{"l":0.1, "r":0.1, "t":0.1, "b":0.1}}, "inch", 96)
        boxW=wh_m[0]
        boxH=wh_m[1]/len(self.colorList)
        fontSize=15
        for i, colorObj in enumerate(self.colorList):
            originalRgb="RGB("+",".join([str(s) for s in self.rgbList[i]])+")"
            y=boxH*i
            svg.addComponent(svg, svg.g, "rect",
                             {"x": 0, "y": y, "width": boxW, "height": boxH,
                              "fill": "none",'stroke':"black"})

            #text original color
            idxText= svg.addComponent(svg, svg.g, "text", {"x":fontSize, "y": fontSize + y, "style": 'font-size:' + str(fontSize) + ';'})
            idxText.string="Tool:"+str(i)+" "+str(originalRgb)
            svg.addComponent(svg, svg.g, "rect",
                             {"x": 0, "y": fontSize*2 + y, "width":boxW,"height":boxH/4,"fill":originalRgb})

            #generate matched color
            if "mixedExpect" not in colorObj:
                #make one grid
                gridWidth=boxW
            else:
                gridWidth=boxW/4
            jy=fontSize*3 + y+boxH/4
            textY=fontSize*3 + y+boxH/2

            for j,cObj in enumerate(colorObj["c"]):
                rgbStrToAppend=TCM.rgbToString(cObj["rgb"])
                jx=j*gridWidth
                svg.addComponent(svg, svg.g, "rect",
                                 {"x": jx, "y": jy, "width": gridWidth, "height": boxH / 4,
                                  "fill": rgbStrToAppend})
                idxText = svg.addComponent(svg, svg.g, "text", {"x": 0, "y": textY + fontSize + j * fontSize, "style": 'font-size:' + str(fontSize * 0.8) + ';'})
                idxText.string = "|".join(["id:"+str(cObj["i"]),"code:"+str(cObj['code']),rgbStrToAppend])
            if "mixedExpect" in colorObj:
                svg.addComponent(svg, svg.g, "rect",
                                 {"x": gridWidth*3, "y": jy, "width": gridWidth, "height": boxH / 4,
                                  "fill": TCM.rgbToString(colorObj["mixedExpect"]),"stroke":"black"})
        #save
        svg.saveSVG(svg, fullPath=self.getFullSaveLoc("tool") + ".svg")
        with open(self.getFullSaveLoc("threadColor")+ ".json", 'w') as outfile:
            json.dump({"colorList":self.colorList,"tools":self.tools}, outfile)
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
        self.rgbList,self.colorList=TCM.pickRandomThreadColor(ct)
        for i in range(ct):
            self.tools[i]["stroke"]="RGB("+",".join([str(s) for s in self.rgbList[i]])+")"
        # print(self.tools)
        print("picked random color:",self.tools)
    def matchColor(self,colorList,allowMix=True):
        '''
        given a color list (list of rgb tuples), match the best thread color and assign to this threadPlotter object
        :param colorList:
        :return:
        '''
        self.rgbList=colorList
        self.plainColor,self.mixedColor,self.colorList=TCM.pickThreadColor(colorList,allowMix=allowMix)
    def __init__(self,settings,batchName="",svg=True,toolSvg=True):
        DirectAuthoringGenerator.__init__(self,settings,batchName=batchName,svg=svg,toolSvg=toolSvg)
        #extract thread plotter specific information from the settings
        self.initSpeedAndDepthMap()
        self.segmentLength=UB.unitConvert(self.currentSpec["segmentLength"],self.unit,self.i2p)
        self.trailStitchLength=UB.unitConvert(self.currentSpec["trailStitchLength"],self.unit,self.i2p)
        self.pickRandomThreadColors()
        self.stitchSetting=self.depthSpeedCalculator(self.segmentLength)
        self.trailStitchSetting=self.depthSpeedCalculator(self.trailStitchLength)
        self.punchGroupCollection=[]
