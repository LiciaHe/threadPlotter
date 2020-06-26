'''
Stores basic settings for a svg-python generator
Includes utility functions for storage and setup
merged version of the DirectAuthoring and the MainGenerator
Dealing with lists and does not check for valid path points
'''

import threadPlotter.Utils.svg as SVG
import threadPlotter.Utils.shapeEditing as SHAPE
import threadPlotter.Utils.basic as UB
import datetime,random

class DirectAuthoringGenerator:
    #storage-related
    def initStorage(self, makeDate=True):
        self.saveLoc = self.baseSaveLoc + self.name + "/"
        UB.mkdir(self.saveLoc)
        # everything is stored here
        if makeDate:
            self.dateFolder = self.saveLoc + str(datetime.datetime.now().strftime("%Y-%m-%d")) + "/"
            UB.mkdir(self.dateFolder)
    def initBasedOnSettings(self, settings, nameKey="name", specKey="spec", basicSettingKey="basic"):
        self.settings = settings
        if nameKey:
            self.name = settings[nameKey]
        else:
            self.name = settings.name
        self.currentSpec = settings[specKey] if specKey else settings.currentSetting

        self.basicSettings = settings[basicSettingKey] if basicSettingKey  else settings.basicSettings

        self.baseSaveLoc=self.settings["baseSaveLoc"] if "baseSaveLoc" in self.settings else ""
        self.initStorage()



        self.timeTag = str(datetime.datetime.now().strftime("%H%M%S")) + "_" + str(random.getrandbits(3))
        self.timedLoc = self.dateFolder + self.timeTag + self.batchName + "/"
        UB.mkdir(self.timedLoc)
        self.unit=self.basicSettings["unit"] if "unit" in self.basicSettings else "inch"
        if "inchToPx" in self.basicSettings:
            self.i2p = self.basicSettings["inchToPx"]
        else:
            self.i2p = 96

    #tools and basic settings
    def generateRandomTools(self, toolCount=-1):
        '''
        random colored tools
        :param toolCount:
        :return:
        '''
        if toolCount < 0:
            toolCount = self.basicSettings["toolsCt"]
        self.tools = []
        for i in range(toolCount):
            self.tools.append({
                "idx": i,
                "stroke-width": 1,
                "stroke": 1,
                "fill": "none"
            })
        ballPenColors = ["#000", "#ff0000", "#8000e8", "#1925ff", "#ffaa00", "#039c2e"]

        if toolCount <= len(ballPenColors):
            bpcSample = random.sample(ballPenColors, toolCount)
        else:
            bpcSample = [random.choice(ballPenColors) for i in range(toolCount)]
        for i in range(toolCount):
            self.tools[i]["stroke"] = bpcSample[i]
    def getRandomToolId(self):
        if hasattr(self, "tools"):
            return random.randint(0, len(self.tools) - 1)
        return -1


    #axidraw-python authoring
    def calculateAxidrawPosition(self,pt,withMargin=True):
        dotPathInInches = SHAPE.ptToInchStrWithTranslate(pt, self.i2p, self.marginInch["l"], self.marginInch["t"])
        if not withMargin:
            dotPathInInches=SHAPE.ptToInchStr(pt,self.i2p,precision=2)
        return dotPathInInches

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
    def addMoveTo(self,dotCenter, writerIdx, withMargin=True):
        dotPathInInches=self.calculateAxidrawPosition(dotCenter,withMargin=withMargin)
        self.axidrawWriters[writerIdx].write("ad.moveto(" + dotPathInInches[0] + "," + dotPathInInches[1] + ")\n")
    def addLineTo(self,pt,writerIdx,withMargin=True):
        dotPathInInches = self.calculateAxidrawPosition(pt, withMargin=withMargin)
        self.axidrawWriters[writerIdx].write("ad.lineto(" + dotPathInInches[0] + "," + dotPathInInches[1] + ")\n")
    def addPath(self,toAppend,d,baseSoup,additionalAttr):
        attr={"d": d}
        attr.update(additionalAttr)
        return SVG.addComponent(baseSoup,toAppend,"path",attr)
    def getSaveName(self, additionalTag=""):
        return self.timeTag + "_" + additionalTag
    def addDrawing(self,pathPoints,writerIdx):
        for i, pt in enumerate(pathPoints):
            if i == 0:
                self.addMoveTo(pt, writerIdx)
            else:
                self.addLineTo(pt,writerIdx)
    def addComment(self, comment, toolIdx):
        self.axidrawWriters[toolIdx].write("##" + comment + "\n")
    def initNewAxidrawWriter(self, additionalTag=""):


        currentName = self.getFullSaveLoc(additionalTag=additionalTag + "_" + str(len(self.axidrawWriters)))

        axidrawWriter = open(currentName + ".py", "w")
        self.axidrawWriters.append(axidrawWriter)
        axidrawWriter.write(self.axidrawHeader)
        self.updateOptions(self.normalSetting, len(self.axidrawWriters) - 1)
        self.writeEmptyUpdate(len(self.axidrawWriters) - 1)
        return len(self.axidrawWriters) - 1


    ##----save---
    def appendToAxidrawCollection(self, pathPoints, toolIdx=-1):
        '''
        adding a path into the path collection
        :param pathPoints:
        :param toolIdx:
        :return:
        '''
        if not hasattr(self, "axidrawPathCollection"):
            self.axidrawPathCollection = []
            for i in range(len(self.tools)):
                self.axidrawPathCollection.append([])
        if toolIdx < 0:
            toolIdx = self.getRandomToolId()

        self.axidrawPathCollection[toolIdx].append(pathPoints)
    def closeFiles(self):
        if hasattr(self, "axidrawPathCollection"):
            for i, coll in enumerate(self.axidrawPathCollection):
                for pathPoints in coll:
                    self.addDrawing(pathPoints, i)
                    self.addDrawing(pathPoints, -1)
                    self.addPath(self.svg.g, SHAPE.getStraightPath(pathPoints), self.svg, self.tools[i])
                    if hasattr(self, "toolSvgs"):
                        self.addPath(self.toolSvgs[i].g, SHAPE.getStraightPath(pathPoints), self.toolSvgs[i],
                                     self.tools[i])
                self.addMoveTo([0, 0], i, withMargin=False)

        for axidrawWriter in self.axidrawWriters:
            axidrawWriter.write("\nad.disconnect()\nprint('end')\n####")
            axidrawWriter.close()

    def saveFiles(self):
        self.closeFiles()
        if hasattr(self, "svg"):
            self.saveSvg(self.svg)
        if hasattr(self, "toolSvgs"):
            for i, s in enumerate(self.toolSvgs):
                self.saveSvg(s, str(i))
    def getFullSaveLoc(self, additionalTag=""):
        return self.timedLoc + self.timeTag + "_" + additionalTag
    def saveSvg(self, soup, additionalTag=""):
        name = self.getFullSaveLoc(additionalTag)
        SVG.saveSVG(soup, fullPath=name + ".svg")

    def __init__(self,settings,batchName="",svg=True,toolSvg=True):
        self.batchName=batchName
        self.initBasedOnSettings(settings)
        self.axidrawWriters = []
        defaultSettings = {
            "normalSetting": {
                "pen_pos_up": 60,
                "pen_pos_down": 20,
                "pen_delay_down": 20,
            },
            "toolsSetting": {
                "pen_pos_up": 100,
                "pen_pos_down": 0,
                "pen_delay_down": 20
            }
        }
        for key in ["normalSetting", "toolsSetting"]:
            if key not in self.basicSettings:
                self.basicSettings[key] = defaultSettings[key]
            else:
                defaultSettings[key].update(self.basicSettings[key])
                self.basicSettings[key] = defaultSettings[key]
        self.normalSetting = self.basicSettings["normalSetting"]
        self.toolsSetting = self.basicSettings["toolsSetting"]
        self.marginInch = self.basicSettings["margins"].copy()
        self.i2p = 96 if "i2p" not in self.basicSettings else self.basicSettings["i2p"]
        if self.i2p!=96:
            print("The inch to pixel rate is currently set to "+str(self.i2p))
        self.toolsCt = self.basicSettings["toolsCt"]

        axidrawHeader = [
            "'''\n auto-generated axidraw code using ThreadPlotter\n'''\nfrom pyaxidraw import axidraw\nimport "
            "time\nad "
            "=axidraw.AxiDraw()\nad.interactive()\nad.connect()\n"
        ]
        for k in self.basicSettings["plotterDefaultSetting"]:
            axidrawHeader.append("ad.options."+k+"="+str(self.basicSettings["plotterDefaultSetting"][k])+"\n")
        axidrawHeader.append("ad.update()\n")
        self.axidrawHeader="\n".join(axidrawHeader)+"\n"



        if svg:
            self.svg, self.wh, self.wh_m, self.boundaryRect, self.margins = SVG.makeBasicSvgWithFoundations(
                self.basicSettings,unit=self.unit,i2p=self.i2p)
            self.generateRandomTools()
            if toolSvg:
                self.toolSvgs=[]
                for i in range(len(self.tools)):
                    svg, wh, whm, br, m = SVG.makeBasicSvgWithFoundations(
                        self.basicSettings,unit=self.unit,i2p=self.i2p)
                    self.toolSvgs.append(svg)
        for i in range(len(self.tools)):
            self.initNewAxidrawWriter()

