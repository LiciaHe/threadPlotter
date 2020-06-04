'''
boundary test for the thread plotter
'''
import sys
sys.path.insert(1,"../../")
# from threadPlotter.ThreadPlotter import ThreadPlotter as TP
from threadPlotter.DirectAuthoringGenerator import DirectAuthoringGenerator as DAG

settings={
    "name":"tp00_boundaryTester",#name of the project
    "basic":{
        #stores settings related to the canvas
        "width":10,#inches
        "height":10,#inches
        "toolsCt": 3,#how many colors
        "margins":{"l":2,"r":2,"t":2,"b":2},#in inches
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
            "depthPercRange":[35,100],#The range(%) that the z axis can move. 100% corresponds to the longest stitch whereas 55,
            "distanceRange":[0.03,0.15] #inches
        }
    }

}

test=DAG(settings)