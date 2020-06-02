'''
 Can export to svg
        Must have margin and width, height setting
        Partially adopted from mainGenerator
        They must share the same dimension


'''
import sys
sys.path.insert(1,"../")
import SvgManipulation.Svg as SVG
import SvgManipulation.pathUtils as PU
import Utils.basic as UB
from Utils.Exportable import Exportable


class Visualizable(Exportable):

    def __init__(self,saveLoc,dimentionSettings,nameTag="",makeDate=True):
        Exportable.__init__(self,saveLoc,defaultFileType="svg",nameTag=nameTag,makeDate=makeDate)

        self.i2p=UB.getOrDefault(dimentionSettings,'i2p',96)
        self.unit=UB.getOrDefault(dimentionSettings,'unit',"px")
        self.width=PU.unitConvert(dimentionSettings["width"],self.unit,self.i2p)
        self.height=PU.unitConvert(dimentionSettings["height"],self.unit,self.i2p)
        self.marginOriginal=UB.getOrDefault(dimentionSettings,"margins",{"l":0,"r":0,"t":0,"b":0})
        self.margins={}
        for k in self.marginOriginal:
            self.margins=PU.unitConvert(self.marginOriginal[k],self.unit,self.i2p)
        self.width_height=[self.width,self.height]
        self.wh_m = [self.width_height[0] -self.margins["l"] - self.margins["r"], self.width_height[1] - self.margins['t'] - self.margins["b"]]

        self.pathStrCollection=[]
        self.tools=[]

    def export(self):
        '''
        aggregate the path pointInfo into the pathPoint
        :return:
        '''
        for i,svgColl in  enumerate(self.pathStrCollection):
            svg=SVG.makeSVGwithBasic(self.width_height, self.margins)
            for j, p in svgColl:
                toolAttr={"d":p.pathStr}
                toolAttr.update(self.tools[p.toolIdx])
                SVG.addComponent(svg,svg.g,"path",toolAttr)
            self.exportingStorage.append(SVG.makeExportReadySvg(svg))

        Exportable.export(self)

