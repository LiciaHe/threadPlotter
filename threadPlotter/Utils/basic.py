
import pickle, json,time,os
import random


def rgbToHex(r,g,b):
    return '#%02x%02x%02x' % (r, g, b)
def uniformFromRange(arr):
    return random.uniform(arr[0],arr[1])
def getRandomHex():
     return "%06x" % random.randint(0, 0xFFFFFF)
def getOrDefault(storage,key,default=None):
    if key in storage:
        return storage[key]
    return default


def mkdir(path):
    if (not os.path.exists(path)):
        os.mkdir(path)
        return True
    return False
def unitConvert(val,unit,i2p=96):
    i2cm=i2p/25.4
    multiplier=1
    if "in" in unit.lower():
        multiplier=i2p
    elif "cm" in unit.lower():
        multiplier=i2cm
    elif "mm" in unit.lower():
        multiplier=i2cm*10
    return multiplier*val

def linearScale(inputVal,domainArr,rangeArr):
    '''
    d3 linearScale
    :param input:
    :param domainArr:
    :param rangeArr:
    :return:
    '''
    inputDiff = domainArr[1] - domainArr[0]
    outputDiff = rangeArr[1] - rangeArr[0]
    if inputVal - domainArr[0] == 0:
        return rangeArr[0]
    return (inputVal - domainArr[0]) / inputDiff * outputDiff + rangeArr[0]
def load_object(fileName):

    with open(fileName, 'rb') as inputF:
        obj = pickle.load(inputF)
        inputF.close()
    return obj
def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
def roundPoint(point):
    return [round(xy,2) for xy in point]