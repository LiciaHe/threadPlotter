'''
threadPlotter is a class that contains all the basic functions for generating a plotter-based punch needle embroidery piece.
One project is associated with one design, and can output to svgs and python files (for Axidraw)
'''

from threadPlotter.DirectAuthoringGenerator import DirectAuthoringGenerator as DirectAuthoringGenerator
import threadPlotter.Utils.basic as UB

class ThreadPlotter(DirectAuthoringGenerator):

    def initSpeedAndDepthMap(self):
        '''
        generate linear mapping functions for the depth and speed
        :return:
        '''
        plotterSettingRange=self.currentSpec["plotterSettingRange"]
        depthRange=plotterSettingRange["depthPercRange"]
        speedRange=plotterSettingRange["speedPercRange"]

        self.depthMapFunc =UB.makeIntLinearMap(depthRange[0],depthRange[1],self.toolsCt)
        self.speedMapFunc =UB.makeIntLinearMap(speedRange[0],speedRange[1],self.toolsCt)


    def __init__(self,settings,batchName="",svg=True,toolSvg=True):
        DirectAuthoringGenerator.__init__(self,settings,batchName=batchName,svg=svg,toolSvg=toolSvg)
        #extract thread plotter specific information from the settings
        self.initSpeedAndDepthMap()
        self.segmentLength=UB.unitConvert(self.currentSpec["segmentLength"],self.unit,self.i2p)
        self.trailStitchLength=UB.unitConvert(self.currentSpec["trailStitchLength"],self.unit,self.i2p)




