''' 
ifc Collada Color Fix program

Small python hack for doing small adjustments to IfcConvert convesion from ifc file to collada
'''    

from IFCLineManager import IFCLineManager
from IFCLineManager2 import IFCLineManager2


import sys
import collada
from daeEffectEditor import DaeEffectEditor

if __name__ == '__main__':

    #print sys.argv[1:]
    args = sys.argv[1:]

    if(len(args)<2):
        print ('2 args needed, give names of ifc and collada files')
        print ('usage: python iccfmain <ifc file> <collada file>')
        sys.exit()

    ifcFileName = args[0]
    colFileName = args[1]

    print ifcFileName, colFileName
    
    ifc = IFCLineManager2(ifcFileName)
    #ifc = IFCLineManager(ifcFileName)
    #print ifc.oldNewFxMap


    dee = DaeEffectEditor(colFileName, ifc)
    
    