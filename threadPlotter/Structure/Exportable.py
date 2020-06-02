'''
Handle the lowest level of exporting
init storage, handling names
'''
import Utils.basic as UB
import datetime,random
class InvalidFileType(Exception):

    def __init__(self, *args):
        if args:
            self.message=args[0]
        else:
            self.message=""
    def __str__(self):
        return self.message+"\n"+str(type(self.message))+"\n This file info is not supported\n"

class Exportable:
    def initStorage(self,saveLoc,makeDate,nameTag):
        self.saveLoc = saveLoc
        self.nameTag=nameTag
        self.timeTag = str(datetime.datetime.now().strftime("%H%M%S")) + "_" + str(random.getrandbits(3))
        self.makeDate=makeDate
        if makeDate:
            dateTag=str(datetime.datetime.now().strftime("%Y-%m-%d"))
            self.dateFolder = self.saveLoc +nameTag+"_"+dateTag+"/"
            UB.mkdir(self.dateFolder)
            self.timedLoc = self.dateFolder + self.timeTag + "/"
        else:
            self.timedLoc = self.saveLoc + self.timeTag + "/"
    def getFullSaveLoc(self,additionalTag=""):
        return self.timedLoc+self.timeTag+"_"+additionalTag
    def getSaveName(self,additionalTag):
        return self.timeTag + "_" + additionalTag
    def export(self):
        for i, info in enumerate(self.exportingStorage):
            ext=UB.getOrDefault(self.fileTypeKey,i,self.defaultFileType)
            nameKey=UB.getOrDefault(self.exportingAdditionalTag,i,"")
            fullName=self.getFullSaveLoc(additionalTag=nameKey)+"_"+str(i)+"."+ext
            if isinstance(info,str):
                with open(fullName,"w") as f:
                    f.write(info)
            elif isinstance(info,object):
                UB.save_object(info,fullName)
            else:
                raise InvalidFileType(info)
    def appendInfoToStorage(self,info,fileType=None,additionalTag=None):
        self.exportingStorage.append(info)
        idx=len(self.exportingStorage)-1
        if fileType:
            self.fileTypeKey[idx]=fileType
        if additionalTag:
            self.exportingAdditionalTag[idx]=additionalTag


    def __init__(self,saveLoc,defaultFileType,nameTag="",makeDate=True):
        self.initStorage(saveLoc,makeDate,nameTag)
        self.exportingStorage=[]# everything in here will be stored. Each value should be either a string or an object (stored as pkl if it's an object)
        self.exportingAdditionalTag={}#used to add additional name tags
        self.fileTypeKey={}#used to add additional file types. Use numerical INDEX(VALUE) as index.
        self.defaultFileType=defaultFileType

