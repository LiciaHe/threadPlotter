'''
boundary test for the thread plotter
'''
import sys
sys.path.insert(1,"../../")
from threadPlotter.TP_utils import shapeEditing as SHAPE

from threadPlotter.ThreadPlotter import ThreadPlotter as TP

settings={
    "name":"tp00_boundaryTester",#name of the project
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
boundaryRect = SHAPE.makeRectPoints(
    0,
    0,
    testPlotter.wh_m[0],
    testPlotter.wh_m[1],
    closed=True
) #making points for a rectangle.
# wh_m is a list that stores the width and height within
#   the plotable area (exclude margin).
# wh_m[0] is the width, and wh_m[1] is the height.
# The value stored is in pixels.
# If you use inch or mm, threadPlotter will convert your settings into px.

testPlotter.initPunchGroup(0, boundaryRect)
#pattern information are going to be stored as
#  PunchGroup instances. The initPunchGroup function takes
#  an id of the thread, and a list of (unprocessed) points


testPlotter.saveFiles()
#ThreadPlotter will process the path you provided
#  by segmenting it and connecting multiple punch groups.
#  Then, it will export svg and python to your selected directory.