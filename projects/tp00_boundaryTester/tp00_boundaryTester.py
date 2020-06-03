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
        "displayOuterRect": False
    },
    "spec":{
        #stores any user-defined specs

    }

}

test=DAG(settings)