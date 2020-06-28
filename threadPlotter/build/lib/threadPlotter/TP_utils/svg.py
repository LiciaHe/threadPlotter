from bs4 import BeautifulSoup
from threadPlotter.TP_utils.basic import unitConvert
import re

svgStarter='<svg width="0" height="0" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"></svg>'
def makeExportReadySvg(baseSoup,repList=None):
    defaultRep = ["path", "rect", "circle", "line", "polygon"]
    if repList:
        defaultRep += repList
    svgStr = baseSoup.prettify()
    for rep in defaultRep:
        if rep in svgStr:
            svgStr = "".join(svgStr.split("</" + rep + ">"))
            pathBackRef = re.compile("(<" + rep + ".*?)(>)")
            svgStr = pathBackRef.sub(r'\1/>', svgStr)
    return svgStr

def saveSVG(baseSoup,fileName=None,saveLoc=None,postTag=None,repList=None,fullPath=None):
    svgStr=makeExportReadySvg(baseSoup,repList)
    if fullPath:
        sl=fullPath
    else:
        sl=saveLoc+fileName+postTag+".svg"
    with open(sl,'w') as saveFile:
        saveFile.write(svgStr)


def makeSvg():
    return BeautifulSoup(svgStarter, "html.parser")

def applyAttrs(soup,attrs):
    for key in attrs:
        soup.attrs[key]=attrs[key]
def makeSVGwithBasic(wh,margins,id="main_g",innerBox=False,outerBox=False):
    svg = makeSvg()
    attrs={
        "width":str(wh[0])+"px","height":str(wh[1])+"px",
        "viewBox":"0 0 "+str(wh[0])+" "+str(wh[1])
    }
    applyAttrs(svg.svg, attrs)
    defs = svg.new_tag("defs")
    svg.svg.append(defs)
    main_g = svg.new_tag("g")
    main_g.attrs = {"id": id, "transform": "translate(" + str(margins["l"]) + "," + str(margins["t"]) + ")"}
    svg.svg.append(main_g)
    if outerBox:
        addComponent(svg, svg.svg, "rect", {
            "x": 0,
            "y": 0,
            "width": wh[0],
            "height": wh[1],
            "fill": "none",
            "stroke": "black",
            "id":"outerBox"
        })
    if innerBox:
        innerRect = svg.new_tag("rect")
        applyAttrs(innerRect, {
            "x": margins["l"],
            "y": margins['t'],
            "width": wh[0]-margins["l"]-margins["r"],
            "height": wh[1]-margins["t"]-margins["b"],
            "fill": "none",
            "stroke": "black",
            "id":"innerBox"
        })
        svg.svg.append(innerRect)


    return svg
def addComponent(soupBase,base,tagName,attrs):
    e = soupBase.new_tag(tagName)
    applyAttrs(e,attrs)
    base.append(e)
    return e

def makeBasicSvgWithFoundations(basicSettings,unit,i2p):
    '''
    SHORTER VERSION, WITHOUT TOOLPAD
    :param basicsettings:
    :return:
    '''
    wkey = "width"
    hKey = "height"
    if "paperWidth" in basicSettings:
        wkey="paperWidth"
        hKey="paperHeight"
    if unit.upper()=="PX":
        width_height=[basicSettings[wkey],basicSettings[hKey]]
    #init svg
    else:
        width_height = [unitConvert(v,unit,i2p) for v in [basicSettings[wkey],basicSettings[hKey]]]

    #make margin box
    margins=basicSettings["margins"].copy()
    for k in margins:
        margins[k] = unitConvert(margins[k], unit, i2p)

    svg = makeSVGwithBasic(width_height, margins)

    boundaryRect = {}
    wh_m = [width_height[0] - margins["l"] - margins["r"], width_height[1] - margins['t'] - margins["b"]]
    # print("wh", width_height, wh_m, margins)
    if("displayOuterRect" in basicSettings and basicSettings["displayOuterRect"]):
        boundaryRect["outer"]=addComponent(svg,svg.svg,"rect",{
            "x":0,
            "y":0,
            "width":width_height[0],
            "height":width_height[1],
            "fill":"none",
            "stroke":"black"
        })

    if("displayInnerRect" in basicSettings and  basicSettings["displayInnerRect"]):
        innerRect=svg.new_tag("rect")
        applyAttrs(innerRect,{
            "x":margins["l"],
            "y":margins['t'],
            "width":wh_m[0],
            "height":wh_m[1],
            "fill":"none",
            "stroke":"black"
        })
        svg.svg.append(innerRect)
        boundaryRect["inner"] = innerRect

    return svg, width_height,wh_m,boundaryRect,margins
