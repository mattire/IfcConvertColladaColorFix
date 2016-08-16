from ifcglobals import *
from utils import *

class IFCDataLine:
    def __init__(self, line):
        spl = line.split('=')
        self.ifcNum   = int(spl[0][1:])
        self.dataType = spl[1][:spl[1].index('(')]
        self.brackets = spl[1][spl[1].index('('):].strip()[0:-1]
        self.refs = []
        self.refTypeMap = {}
        if (self.dataType in interestingNodes):
            self.findRefs()
        
    def argConstruct(cls, dn, type, brackets):
        cls.dn = dn
        cls.dataType = type
        cls.brackets = brackets
        return cls

    def getNameIfExists(self):
        obj = stripBrackets(self.brackets).split(',')[0]
        if type(obj) is str: return obj[1:-1]
        else: return None

    def printSelf(self):
        for k in self.__dict__.keys(): print (self.__dict__[k])
    
    def findRefs(self):
        ends = [i for i, x in enumerate(self.brackets) if x in [',',')']]
        begings = [i for i, x in enumerate(self.brackets) if x in ['#']]
        for b in begings:
            end = [e for e in ends if e > b][0]
            self.refs.append(int(self.brackets[b:end][1:]))
        
    def getRefTypes(self, dataList):
        self.refTypeMap = {}
        for ref in self.refs:
            refElemType = dataList[ref].dataType
            if refElemType in self.refTypeMap: self.refTypeMap[refElemType].append(ref)
            else: self.refTypeMap[refElemType] = [ref]


