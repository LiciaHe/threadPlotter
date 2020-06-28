
import pyclipper


OFFSETTYPES={
    "CLOSEDPOLYGON":pyclipper.ET_CLOSEDPOLYGON,
    "CLOSEDLINE":pyclipper.ET_CLOSEDLINE,
    "OPENROUND":pyclipper.ET_OPENROUND,
    "OPENSQUARE":pyclipper.ET_OPENSQUARE,
    "OPENBUTT":pyclipper.ET_OPENBUTT
}
JOINTTYPES={
    "MITER":pyclipper.JT_MITER,
    "ROUND":pyclipper.JT_ROUND,
    "SQUARE":pyclipper.JT_SQUARE
}
CLIPPER_TYPE={"intersection":pyclipper.CT_INTERSECTION,"union":pyclipper.CT_UNION,"difference":pyclipper.CT_DIFFERENCE,"xor":pyclipper.CT_XOR}
FILL_TYPE={"evenodd":pyclipper.PFT_EVENODD,"positive":pyclipper.PFT_POSITIVE,"negative":pyclipper.PFT_NEGATIVE,"nonzero":pyclipper.PFT_NONZERO}


def makeOffset(subjPoints,offset_width,offsetType="CLOSEDPOLYGON",jointType="MITER"):
    '''
    http://www.angusj.com/delphi/clipper/documentation/Docs/Units/ClipperLib/Types/EndType.htm
    http://www.angusj.com/delphi/clipper/documentation/Docs/Units/ClipperLib/Types/JoinType.htm
    :param subjPoints:
    :param offset_width:
    :return:
    '''
    offsetType=OFFSETTYPES[offsetType.upper()]
    jointType=JOINTTYPES[jointType.upper()]
    pco = pyclipper.PyclipperOffset()
    sub_s=pyclipper.scale_to_clipper(subjPoints)
    pco.AddPath(sub_s,jointType, offsetType)
    solution = pco.Execute(pyclipper.scale_to_clipper(offset_width))
    return pyclipper.scale_from_clipper(solution)




def makeClipper(subjs,clip,clipperTypeStr,s_fill_key="positive",c_fill_key="positive",subjClosed=True,s_multi=False,c_multi=False):
    '''

    :param subjs:
    :param clip: window to be used for the cut
    :param clipperTypeStr:
    :param s_fill_key:
    :param c_fill_key:
    :param subjClosed:
    :param s_multi:
    :param c_multi:
    :return:
    '''
    pc = pyclipper.Pyclipper()
    scaledSubj = pyclipper.scale_to_clipper(subjs)
    scaledClip = pyclipper.scale_to_clipper(clip)
    # print("clip",scaledClip)
    clipperType = CLIPPER_TYPE[clipperTypeStr]
    if s_multi:
        pc.AddPaths(scaledSubj, pyclipper.PT_SUBJECT, subjClosed)
    else:
        pc.AddPath(scaledSubj, pyclipper.PT_SUBJECT, subjClosed)
    if c_multi:
        pc.AddPaths(scaledClip, pyclipper.PT_CLIP, True)
    else:
        pc.AddPath(scaledClip, pyclipper.PT_CLIP, True)
    fill1=FILL_TYPE[s_fill_key]
    fill2=FILL_TYPE[c_fill_key]
    flattenPaths = []
    solution = pc.Execute2(clipperType, fill1, fill2)
    paths = pyclipper.PolyTreeToPaths(solution)
    # print(paths)
    for p in paths:
        flattenPaths.append(pyclipper.scale_from_clipper(p))
    return flattenPaths

