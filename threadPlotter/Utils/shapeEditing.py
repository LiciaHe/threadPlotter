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