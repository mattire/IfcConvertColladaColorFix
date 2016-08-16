from ifcglobals import *
from utils import *
import sys
import traceback

from IFCDataLine import IFCDataLine


        

class RelationColorTree(object):

    #class RecursionVars():
    #    def __init__(self, path, pathInd, targetList, currentElem):
    #        self.path       = path
    #        self.pathInd    = pathInd
    #        self.targetList = targetList
    #        self.currentElem= currentElem
    

    def __init__(self, relDL, dataLineList):
        self.dataLineList = dataLineList
        self.relDL = relDL
        self.relDL.getRefTypes(self.dataLineList)

        # recursively created trees: (first element is the relDL)
        self.colorRoot                      = [] # not really needed
        self.colorRootEndElems              = []
        self.representationBranches         = [] # not really needed
        self.representationBranchesEndElems = []

        self.colorRoot = self.findPathElems(colorRootPath, 
                            0,     
                            self.colorRootEndElems,
                            self.relDL)

        self.representationBranches = self.findPathElems( representationBranchPath , 
                            0, 
                            self.representationBranchesEndElems,
                            self.relDL)
        
        #print [c.brackets for c in self.colorRootEndElems]
        #print [c.brackets for c in self.representationBranchesEndElems]
        self.parseColors()
        self.parseRepresentations()
        #print self.rgb
        #print self.representationNum
        #print self.ifcType
        #if self.representationNum == 0:
        #    print 'ifcNum:', self.relDL.ifcNum
        #print 'end'
        

    def parseColors(self):
        firstAndThirdElem = lambda brackets : [stripBrackets(brackets).split(',')[i] for i in [0,2]]
        tupleToColorAndInt = lambda t : (t[0][1:-1], int(t[1][t[1].index('(')+1:t[1].index(')')]))
        blist = [c.brackets for c in self.colorRootEndElems]
        self.color = [tupleToColorAndInt(firstAndThirdElem(b)) for b in blist]
        r = [t[1] for t in self.color if t[0]=='Red'][0]
        g = [t[1] for t in self.color if t[0]=='Green'][0]
        b = [t[1] for t in self.color if t[0]=='Blue'][0]
        self.rgb = (r,g,b)

    def parseRepresentations(self):
        isNotBoundingBoxModel = lambda elem: stripBrackets(elem.brackets).split(',')[2][1:-1] != 'BoundingBox'
        
        self.representationNum = 0
        repNums = [e.ifcNum for e in self.representationBranchesEndElems if isNotBoundingBoxModel(e)]
        if len(repNums)!=0:
            self.representationNum = repNums[0]
        
        branch = self.representationBranches[1]
        if(branch!=[]):
            self.ifcType = branch[0][0].dataType
        else:
            self.ifcType = None

        
    def findPathElems(self, path, pathInd, endElemList, currentElem):
        currentElem.getRefTypes(self.dataLineList)
        if(pathInd>=len(path)):
            endElemList.append(currentElem)
            return ()
        pathSequenceObj = path[pathInd]
        parsedList = []
        if(pathInd<=len(path)):
            try:
                currentElem.getRefTypes(self.dataLineList)
                if type(pathSequenceObj) is tuple:
                    parsedList = self.handlePathTuple(path, pathInd, endElemList, currentElem, pathSequenceObj)
                elif type(pathSequenceObj) is list:
                    parsedList = self.handlePathList(path, pathInd, endElemList, currentElem, pathSequenceObj)
            except Exception as ex:
                print '*************************'
                print 'recursion failure'
                traceback.print_exc()
                print dir(ex)
                sys.exit()
        return (currentElem, parsedList)

    def handlePathTuple(self, path, pathInd, endElems, currentElem, seqTuple):
        nextType = seqTuple[0]
        nextName = seqTuple[1]
        #print '****'
        #currentElem.printSelf()
        nextElemPtrs = currentElem.refTypeMap[nextType]
        nextElems = []
        if nextName != None:
            nextElems = [self.dataLineList[nep] for nep in nextElemPtrs \
                                if self.dataLineList[nep].getNameIfExists() == nextName]
        else:
            nextElems = [self.dataLineList[nep] for nep in nextElemPtrs]
        results = []
        for e in nextElems:
            pathInd +=1
            res = self.findPathElems(path,pathInd, endElems, e)
            results.append((e, res))
            #if pathInd == len(path):
            #    endElems.append(currentElem)
        return results

    def handlePathList(self, path, pathInd, endElems, currentElem, seqList):
        results = []
        availableTypesAndNames = [s for s in seqList if s[0] in currentElem.refTypeMap.keys()]
        #for seqTuple in seqList:
        for seqTuple in availableTypesAndNames:
            results.extend(self.handlePathTuple(path, pathInd, endElems, currentElem, seqTuple))
        return results
