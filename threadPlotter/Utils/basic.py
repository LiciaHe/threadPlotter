
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