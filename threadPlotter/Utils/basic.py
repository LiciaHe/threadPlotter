
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

def makeIntLinearMap(rangeMin,rangeMax,domainCount):
    '''
    goes
    :param rangeMin:
    :param rangeMax:
    :param domainCount: a list of mapped values that goes from low to high
    :return:
    '''
    dist=(rangeMax-rangeMin)/domainCount
    #[int(rangeMax - i * dist) for i, c in range(domainCount)]
    return lambda i:rangeMax-i*dist if i<domainCount and i>-1 else None
def load_object(fileName):

    with open(fileName, 'rb') as inputF:
        obj = pickle.load(inputF)
        inputF.close()
    return obj
def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
