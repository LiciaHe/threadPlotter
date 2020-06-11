'''
stores utility functions for embroidery-specific calculations
'''
import threadPlotter.Utils.shapeEditing as SHAPE
import threadPlotter.Utils.basic as UB
def makeConnectedDot(pathPoints,segmentLength,minDist):
    '''
    converted from "convertPathsToConnectedDots"
    create punch needle points by
    keep spliting line.Will check minimal distance
    :param pathPoints:
    :param segmentLength:
    :return:
    '''
    dotCenters=[]
    for i, pt in enumerate(pathPoints):
        if i==0:
            continue
        pt0=pathPoints[i-1]
        dotCenters += SHAPE.splitSingleLine([pt0, pt], segmentLength,toPoint=True)

    i=1
    while i <len(dotCenters)-1:
        j=i+1
        if SHAPE.calculateDistBetweenPoints(dotCenters[i],dotCenters[j])<minDist:
            dotCenters[i]=SHAPE.getMidPoint(dotCenters[i],dotCenters[j])
            dotCenters.pop(j)
        else:
            i+=1
    return dotCenters