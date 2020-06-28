'''
boundary test for the thread plotter
'''
import sys
sys.path.insert(1,"../../")
from threadPlotter.ThreadPlotter import ThreadPlotter as TP
from threadPlotter.TP_punchneedle.GridImgConverter import GridImgConverter
from threadPlotter.TP_punchneedle.threadColorManagement import rgbStrToTriplet
settings={
    "name":"tp02_convertImg",#name of the project
    "baseSaveLoc":"C:/licia/art/generative/", #specify where to save the generated files
    "basic":{
        #stores settings related to the canvas
        "width":10,#inches
        "height":10,#inches
        "toolsCt": 3,#how many colors
        "margins":{"l":2,"r":2,"t":2,"b":2},#in inches
        "unit": "inch",  # support px, inch and mm.
        "displayInnerRect": False, #adding a boundary rectangle to the svg file (will not append to the python files)
        "displayOuterRect": False,
        "plotterDefaultSetting":{
            "model":2 #according to https://axidraw.com/doc/py_api/#model
        }
    },
    "spec":{
        #stores any user-defined specs
        "segmentLength":0.04,#inches
        "trailStitchLength":0.15,
        "trailLoopDepthPerc":35,
        "plotterSettingRange":{
            "speedPercRange":[20,80],
            "depthPercRange":[35,100],#The range(%) that the z axis can move. 100% corresponds to the longest stitch whereas 55% corresponds to the shortest stitch
            "distanceRange":[0.03,0.15] #inches
        }
    }
}

testPlotter=TP(settings) #create an instance
#construct a list of random colors
imageName="1200px-Apple-tree_blossoms_2017_G3.jpg"
gic=GridImgConverter(
    imgLoc="", #stored in the same folder
    imgName=imageName,
    colorCount=testPlotter.toolsCt,
    imgSize=testPlotter.wh_m,
    pixelization_length=testPlotter.segmentLength
)

pathByColor=gic.exportOrderedGrid()
colorListRGBstr=pathByColor.keys()
colorList=[rgbStrToTriplet(rgbStr) for rgbStr in colorListRGBstr]
testPlotter.matchColor(colorList)
for toolI,colorKey in enumerate(colorListRGBstr):
    for path in pathByColor[colorKey]:

        testPlotter.initPunchGroup(
            toolI,
            path,
            skipSegment=True
        )

gic.saveImg(testPlotter.getFullSaveLoc("processedImg_"))

testPlotter.saveFiles()#export
