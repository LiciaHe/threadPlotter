from svgpathtools import parse_path,Line, Path
import threadPlotter.Utils.basic as UB
import math

def getMidPoint(pt1,pt2):
    return [(pt1[0]+pt2[0])/2,(pt1[1]+pt2[1])/2]
def ptToInchStr(pt,i2p,precision=None):
    if precision:
        [str(round(float(xy) / i2p,precision)) for xy in pt]
    return [str(float(xy)/i2p) for xy in pt]
def ptToInchStrWithTranslate(pt,i2p,xtrans,ytrans):
    return [str(round(float(pt[0]/i2p+xtrans),2)),str(round(float(pt[1])/i2p+ytrans,2))]
def roundPoint(point):
    return [round(xy,2) for xy in point]
def getBoundaryBoxPtsVersion(pathPoint):
    '''
    RETURN MINMAX
    :param pathPoint:
    :return:
    '''
    minX=min([xy[0] for xy in pathPoint])
    maxX=max([xy[0] for xy in pathPoint])
    minY=min([xy[1] for xy in pathPoint])
    maxY=max([xy[1] for xy in pathPoint])
    return minX,maxX,minY,maxY
def getBoundaryWHversion(pathPoint):
    '''
    return x,y,w,h
    :param pathPoint:
    :return:
    '''
    return ptBBoxToWHbbox(getBoundaryBoxPtsVersion(pathPoint))
def pressIntoABox(points,xmin,ymin,xmax,ymax):
    '''
    in place change so that nothing goes out of boundary
    :param points:
    :param xmin:
    :param ymin:
    :param xmax:
    :param ymax:
    :return:
    '''
    for p in points:
        x,y=p
        if x < xmin:
            p[0] = xmin
        if y < ymin:
            p[1] = ymin
        if x > xmax:
            p[0] = xmax
        if y > ymax:
            p[1] = ymax
def getStraightPath(pointArr,closed=False):
    p="M"+" L".join([",".join([str(round(l,2)) for l in xy[:2]]) for xy in pointArr])
    if closed:
        return p+"Z"
    return p
def splitSingleLine(start_end,unitLength,toPoint=False):
    '''
    return strings
    :param start_end:
    :param unitLength:
    :return:
    '''
    if UB.pointEquals(start_end[0],start_end[-1]):
        return []
    pathStr=getStraightPath(start_end)
    path=parse_path(pathStr)
    try:
        l=path.length()
        if l>unitLength:
            paths=[]
            t=unitLength/l
            ts=0
            te=t
            for i in range(int(math.ceil(l/unitLength))):
                seg=Line(path.point(ts),path.point(te))
                p=Path(seg)
                if toPoint:
                    paths.append([UB.getPointFromComplex(path.point(ts)), UB.getPointFromComplex(path.point(te))])
                else:
                    paths.append(p.d())

                ts+=t
                te+=t
                te=min(1,te)
            if toPoint:
                paths.append(
                    [UB.getPointFromComplex(path.point(te)), UB.getPointFromComplex(path.point(1))])
            else:
                paths.append(getStraightPath([UB.getPointFromComplex(path.point(te)),UB.getPointFromComplex(path.point(1))]))
            return paths
        if toPoint:
            return [start_end]
        else:
            return [pathStr]
    except Exception as e:
        print(start_end,"something wrong with the splitLine",e)
        return []
def calculateDistBetweenPoints(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
def calculatePathLength(pathPoints):
    l=0
    if len(pathPoints)<2:
        return l
    for i in range(1,len(pathPoints)):
        l+=calculateDistBetweenPoints(pathPoints[i-1],pathPoints[i])
    return l
def makeRectPoints(x,y,w,h,closed=False):
    pts=[[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
    if closed:
        pts.append([x,y])
    return pts
