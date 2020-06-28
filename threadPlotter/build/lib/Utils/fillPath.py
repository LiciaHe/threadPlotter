'''
package to fill things
'''
import math,re,random
import threadPlotter.Utils.shapeEditing as SHAPE


def convertLinePathToDots(linePts,gap,innerDist=1,masterBoundary=None,addGap=False,locOnly=False):
    lines=[]
    for i, pt in enumerate(linePts):
        if i==0:
            continue
        pt0=linePts[i-1]
        if pt0!=None:
            #TODO : there shouldn't be a none
            lines += SHAPE.splitSingleLine([pt0, pt], gap)
    pointPaths=[]
    prevEnd=None
    appendGap=False
    for line in lines:
        start, middle, endTag, end = PO.parseToStartAndEnd(line)
        startPt = [round(float(xy), 2) for xy in start.split(",")]
        endPt = [xy + innerDist for xy in startPt]

        if masterBoundary==None or (masterBoundary!=None and  PO.ptWithinRect(masterBoundary[0],masterBoundary[1],masterBoundary[2],masterBoundary[3],startPt)):
            if appendGap:
                newLine=[prevEnd,startPt]
                gapLine,gapPointPaths=convertLinePathToDots(newLine,gap,innerDist,masterBoundary=masterBoundary,addGap=addGap,locOnly=locOnly)
                pointPaths+=gapPointPaths
            path = SHAPE.getStraightPath([startPt, endPt])
            if locOnly:
                path=startPt.copy()
            pointPaths.append(path)
            prevEnd = startPt
            appendGap=False
        elif addGap:
            appendGap=True

    return lines,pointPaths

def makeTinyDot_pathPoints(startPt,innerDist=1):
    endPt = [xy + innerDist for xy in startPt]
    return [startPt, endPt]


def convertPathsToConnectedDots(pathPoints,boundaryRect=None,dotDistance=5,locOnly=False):
    '''
    create punchNeedle ready path. connect all paths together into one, and change it to dots
    :param pathPoints:(x,y,w,h,
    :return:
    '''
    connectedPathPoint=[]
    for pathP in pathPoints:
        connectedPathPoint += pathP
    line,pointPaths=convertLinePathToDots(connectedPathPoint,dotDistance,masterBoundary=boundaryRect,addGap=True,locOnly=locOnly)
    return line,pointPaths

def getPunchNeedleReadyDot(pathPoints,boundaryRect,dotDistance=4,addTrail=True,minDistance=2):
    '''
    required boundaryRect
    Rule: 1) min/max distance is controlled
    2) try to reduce duplication
    :param pathPoint:
    :param boundaryRect: (x,y,w,h,
    :param addTrail: add returning trail
    :return:
    '''
    if addTrail:
        pathPoints.append([pathPoints[-1][-1],[0,0]])
    line, pointPaths=convertPathsToConnectedDots(pathPoints,boundaryRect,dotDistance=dotDistance,locOnly=True)
    i=1
    while i <len(pointPaths)-1:
        j=i+1
        if PU.calculateDistBetweenPoints(pointPaths[i],pointPaths[j])<minDistance:
            pointPaths[i]=PU.getMidPoint(pointPaths[i],pointPaths[j])
            pointPaths.pop(j)
        else:
            i+=1
    return pointPaths






