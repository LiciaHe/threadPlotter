'''
boundary test for the thread plotter
'''
import sys
sys.path.insert(1,"../../")
from threadPlotter.Utils import shapeEditing as SHAPE

from threadPlotter.ThreadPlotter import ThreadPlotter as TP
import random
settings={
    "name":"tp01_circleTester",#name of the project
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
colorList=[]
for i in range(3):
    rgb=[random.randint(0,255) for j in range(3)]
    colorList.append(rgb)

maxSize=min(testPlotter.wh_m)/2 #largest circle radius
minSize=10 #smallest circle radius
gap=8 #gap between each circle
circleCt=int((maxSize-minSize)/gap)# how many circles we are going to draw

for i in range(circleCt):
    r=minSize+i*gap
    circle=SHAPE.makeUniformPolygon(testPlotter.wh_m[0]/2,testPlotter.wh_m[1]/2,r,50,closed=True) #approximate a circle with a 50 side polygon
    colorId=testPlotter.getRandomToolId()
    testPlotter.initPunchGroup(colorId, circle) #get a random color and store it

testPlotter.saveFiles()#export