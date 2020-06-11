'''
PROCESS and find colored thread
'''
import math,random

from threadPlotter.Utils import basic as UB
from itertools import combinations

def getAverageColor(c1,c2,c3):
    '''
    return avg rgb
    :param c1: 0-255 triplets
    :param c2:
    :param c3:
    :return:
    '''

    comb=[c1,c2,c3]
    r=sum([c[0]**2 for c in comb])
    g=sum([c[1]**2 for c in comb])
    b=sum([c[2]**2 for c in comb])

    return (int(math.sqrt(r / 3.0)), int(math.sqrt(g / 3.0)), int(math.sqrt(b / 3.0)))

def calculateColorDifference(c1,c2):
    '''

    :param c1: rgb triplets
    :param c2:
    :return:
    '''
    return ((c1[0] - c2[0]) * 0.30)**2+((c1[1] - c2[1]) * 0.59)**2+((c1[2] - c2[2]) * 0.11)**2

def makeColorCombinations(seedFile="embroidery_thread_color.csv"):
    '''
    take the csv for embroidery thread color and build a python pkl. store locally
    :return:
    '''
    originalColor=[]
    i=0
    with open(seedFile,"r") as seed:
        for row in seed:
            if "name" in row or "," not in row:
                continue
            content=row.strip().split(",")
            c={
                "i":i,
                "rgb":(int(content[3]),int(content[4]),int(content[5])),
                "code":content[1],
                "name":content[2]
            }
            i+=1
            originalColor.append(c)
    UB.save_object({"original": originalColor}, "original_only.pkl")
    combs=combinations(list(range(i))*3,3)
    combinedColor=[]
    for c1i,c2i,c3i in combs:
        c1=originalColor[c1i]["rgb"]
        c2=originalColor[c2i]["rgb"]
        c3=originalColor[c3i]["rgb"]
        avgColor=getAverageColor(c1,c2,c3)
        combinedColor.append(((c1i,c2i,c3i),avgColor))
    print(len(combinedColor))
    UB.save_object({"original":originalColor,"mixed":combinedColor},"threadColor.pkl")
def rgbStrToTriplet(rgbStr):
    return [int(c) for c in rgbStr[4:-1].split(",")]
def rgbToString(rgb):
    return "rgb("+",".join([str(int(c)) for c in rgb])+")"
# makeColorCombinations()
def pickThreadColor(colors):
    '''

    :param colors: a list of rgb tuple
    :param additional: decide whether to load additional info
    :return:plainColor,mixedColor,colorList
    '''
    # file="original_only.pkl"
    # if additional:
    file="threadColor.pkl"
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
        if d<distLimit:
            plainColor[i]=selectedOriginal
            colorList.append({"c":[colorMap["original"][0]]})
        else:
            colorMap["mixed"].sort(key=lambda c: calculateColorDifference(c[1], color))
            selectedMixColor = colorMap["mixed"][0]

            mixedColor[i]=selectedMixColor
            obj={"mixedExpect":selectedMixColor[1],"c":[colorMap["original"][idx] for idx in selectedMixColor[0]],"diff":[calculateColorDifference(color, selectedMixColor[1]),calculateColorDifference(colorMap["mixed"][-1][1], color)]}
            colorList.append(obj)

    return plainColor,mixedColor,colorList
def exportThreadColorListPKL(seedFile="embroidery_thread_color.csv"):
    '''
    export list of thread accordingn to settings according to here:
    https://pypi.org/project/pyembroidery/
    :return:
    '''
    originalColor=[]
    i=0
    with open(seedFile,"r") as seed:
        for row in seed:
            if "name" in row or "," not in row:
                continue
            content=row.strip().split(",")
            c={
                "id":i,
                "color":(int(content[3]),int(content[4]),int(content[5])),
                "code":content[1],
                "name":content[2],
                "brand":"NEWBROTHREAD"
            }
            i+=1
            originalColor.append(c)
    UB.save_object(originalColor, "original_thread_list.pkl")
def pickRandomRGBtuple(ct):
    colors=[]
    for i in range(ct):
        colors.append([random.randint(0,255) for c in range(3)])
    return colors
def pickRandomThreadColor(ct):
    colors=pickRandomRGBtuple(ct)
    return pickThreadColor(colors)
if __name__=="__main__":
    exportThreadColorListPKL()


