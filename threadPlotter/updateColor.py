import TP_utils.basic as UB
from itertools import combinations
import math
def exportThreadColorListPKL(seedFile="TP_punchneedle/embroidery_thread_color.csv"):
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
    UB.save_object(originalColor, "TP_punchneedle/original_thread_list.pkl")

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
def makeColorCombinations(seedFile="TP_punchneedle/embroidery_thread_color.csv"):
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
    UB.save_object({"original": originalColor}, "TP_punchneedle/original_only.pkl")
    combs=combinations(list(range(i))*3,3)
    combinedColor=[]
    for c1i,c2i,c3i in combs:
        c1=originalColor[c1i]["rgb"]
        c2=originalColor[c2i]["rgb"]
        c3=originalColor[c3i]["rgb"]
        avgColor=getAverageColor(c1,c2,c3)
        combinedColor.append(((c1i,c2i,c3i),avgColor))
    print(len(combinedColor))
    UB.save_object({"original":originalColor,"mixed":combinedColor},"TP_punchneedle/threadColor.pkl")

if __name__=="__main__":
    makeColorCombinations()
