
import collada
import sys
from IFCLineManager import IFCLineManager
from daeEffectEditor import DaeEffectEditor

def writeToFile(list): 
	with open('temp.txt','w') as txtFile:
		lstr = str(list)
		txtFile.write(lstr)

def printDD(d):
	for k in d.keys():
		print (k)
		for kk in d[k].keys():
			print (kk), d[k][kk]


mesh = collada.Collada('test0.dae')

ids = [m.id.split('-')[0].upper() for m in mesh.effects]

# print ids

ifc = IFCLineManager('301110FJK-Project-Final.ifc')
tps = ifc.getTypesLines(ids)

# print len(tps)
# print len(tps[tps.keys()[13]])

elem = tps[tps.keys()[0]][0]

# print dir(elem)
# print elem.__dict__
# print len(ifc.relLines)
# print ifc.__dict__.keys()

# print ifc.oldNewFxMap

# print ifc.oldNewFxMap


# printDD(ifc.oldNewFxMap)
# sys.exit()
# print '...'
# print ifc.elemsWithColor
# print '...'
# print ifc.typesWithColor
# print '...'
# print ifc.elemsWithType
# print '...'
# print ifc.elemColor
dee = DaeEffectEditor('1.dae', ifc) 	


# print dee.daeColors

# for r in ifc.relations: 
	# print r.DLParent.dataType
	# if 'rgb' in r.PropSet.__dict__.keys():
		# print r.PropSet.rgb
		
	# else:
		# print 'no rgb'