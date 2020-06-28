'''
PROCESS and find colored thread
'''
import random

from TP_utils import basic as UB



def calculateColorDifference(c1,c2):
    '''

    :param c1: rgb triplets
    :param c2:
    :return:
    '''
    return ((c1[0] - c2[0]) * 0.30)**2+((c1[1] - c2[1]) * 0.59)**2+((c1[2] - c2[2]) * 0.11)**2


def rgbStrToTriplet(rgbStr):
    return [int(c) for c in rgbStr[4:-1].split(",")]
def rgbToString(rgb):
    return "rgb("+",".join([str(int(c)) for c in rgb])+")"
# makeColorCombinations()
def pickThreadColor(colors,allowMix=True):
    '''

    :param colors: a list of rgb tuple
    :param additional: decide whether to load additional info
    :return:plainColor,mixedColor,colorList
    '''
    # file="original_only.pkl"
    # if additional:
    file="../../threadPlotter/TP_punchneedle/threadColor.pkl"
    colorMap=UB.load_object(file)
    plainColor={}
    mixedColor={}
    distLimit=80
    colorList = []
    for i,color in enumerate(colors):
        print("picking color",i)
        colorMap["original"].sort(key=lambda c:calculateColorDifference(c["rgb"],color))
        selectedOriginal=colorMap["original"][0]["rgb"]
        d=calculateColorDifference(selectedOriginal,color)
        if d<distLimit or not allowMix:
            plainColor[i]=selectedOriginal
            colorList.append({"c":[colorMap["original"][0]]})
        else:
            colorMap["mixed"].sort(key=lambda c: calculateColorDifference(c[1], color))
            selectedMixColor = colorMap["mixed"][0]

            mixedColor[i]=selectedMixColor
            obj={"mixedExpect":selectedMixColor[1],"c":[colorMap["original"][idx] for idx in selectedMixColor[0]],"diff":[calculateColorDifference(color, selectedMixColor[1]),calculateColorDifference(colorMap["mixed"][-1][1], color)]}
            colorList.append(obj)

    return plainColor,mixedColor,colorList


def pickRandomThreadColor(ct):
    file = "../../threadPlotter/TP_punchneedle/threadColor.pkl"
    colorMap = UB.load_object(file)
    colorList = []
    rgbList=[]

    for i in range(ct):
        pick=random.choice(colorMap["original"])
        colorList.append({"c":[pick]})
        rgbList.append(pick["rgb"])


    return rgbList,colorList


