
from ifcglobals import *
from utils import *
import sys
import traceback

from IFCDataLine import IFCDataLine
from IFCRelationColorTree import RelationColorTree




class IFCLineManager2(object):
    """
    Find relations and recursively go thru ifc lines, using
    predefined paths
    """

    def __init__(self, fName):
        lines = None
        with open(fName) as ifcFile:
            lines = ifcFile.readlines()
        numLines= lines[7:-2]        
        self.dataLines = [IFCDataLine(line) for line in numLines]

        self.dataList = [None] * (self.dataLines[-1].ifcNum + 1)        
        for dl in self.dataLines: self.dataList[dl.ifcNum]=dl 
       
        self.initRelations()
        self.initOldNewFxMap()
        #print self.oldNewFxMap
    
    def initRelations(self):
        self.relLines     = [line for line in self.dataLines if line.dataType=='IFCRELDEFINESBYPROPERTIES']
        #self.relations     = [IFCRelation(rl,self) for rl in self.relLines]
        self.relations     = [RelationColorTree(rl,self.dataList) for rl in self.relLines]
        
        # relation relevant args: ifcType, rgb, representationNum
        self.type_rgb_rep = [(r.ifcType, r.rgb, r.representationNum) for r in self.relations]    

    def initOldNewFxMap(self):
        self.types = list(set([t[0] for t in self.type_rgb_rep]))
        self.colorsWithType = {t:list(set(trr[1] for trr in self.type_rgb_rep if trr[0]==t)) for t in self.types}
        self.oldNewFxMap = {}
        for ifcType in self.colorsWithType.keys():
            if ifcType in byPassList or ifcType == None:
                continue
            newTypesAndColors = {ifcType+ str(e[0]): e[1] for e in enumerate(self.colorsWithType[ifcType])}
            # for each newType select reps with type == ifcType and color == newTypeColor
            map = {}
            for newType, Color in newTypesAndColors.iteritems():
                reps = [trr[2] for trr in self.type_rgb_rep if ifcType==trr[0] and Color==trr[1]]
                map[newType]=(Color, reps)
            self.oldNewFxMap[ifcType]=map    

    def getElementNewMaterial(self, representationKey, oldMaterialName):
        newTypes = self.oldNewFxMap[oldMaterialName.upper()].keys()
        for nt in newTypes:
            tup = self.oldNewFxMap[oldMaterialName.upper()][nt.upper()]
            if representationKey in tup[1]:
                return nt
        return None
