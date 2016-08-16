#IFCCONNECTEDFACESET
#IFCFACEBASEDSURFACEMODEL
#IFCSHAPEREPRESENTATION
#IFCPRODUCTDEFINITIONSHAPE  IFCFURNISHINGELEMENT *
#IFCBUILDINGELEMENTPROXY  **
#IFCRELDEFINESBYPROPERTIES connects building element proxy to propertyset
#IFCPROPERTYSET is set of single and complex propertysets
#IFCCOMPLEXPROPERTY can be color property set
# => make list of:
#	-all building element proxies
#	-all rel defines by properties

def enum(**enums):
    return type('Enum', (), enums)

IfcTypeStrings = 	enum(BldElemProxy	= 'IFCBUILDINGELEMENTPROXY',\
						Relation 		= 'IFCRELDEFINESBYPROPERTIES',\
						PropertySet		= 'IFCPROPERTYSET',\
						Complex			= 'IFCCOMPLEXPROPERTY',\
						Single			= 'IFCPROPERTYSINGLEVALUE')
	
def getFileLines(name):
	f=open('301110FJK-Project-Final.ifc','r')
	lines = f.readlines()
	f.close()
	return lines

class RgbColor:
	def __init__(self, id, r, g, b):
		self.id = id
		self.r = r
		self.g = g
		self.b = b
	
class IFCDataLine:
	def __init__(self, dn, type, brackets):
		self.ifcNum = dn
		self.dataType = type
		self.brackets = brackets
		
	def getReferences(self):
		#self.brackets
		pass
		
	
	
class IFCLineManager:
	def __init__(self, lines):
		numLines= lines[7:-2]		
		dataLines = [self.parseDataLine(line) for line in numLines]
		
		# data list: all the data lines (IFCDataLine) organized
		self.dataList = [None] * dataLines[-1].ifcNum
		for dl in dataLines: self.dataList[dl.ifcNum-1]=dl
		
		self.BldElemProxys 	= [dl for dl in self.dataList \
							   if dl!=None and dl.dataType == IfcTypeStrings.BldElemProxy]
							   
		# self.Relations 		= [dl for dl in self.dataList if dl.dataType == IfcTypeStrings.Relation]
		# self.PropertySets 	= [dl for dl in self.dataList if dl.dataType == IfcTypeStrings.PropertySet]
		
	def parseDataLine(self, line):
		spl = line.split('=')
		ifcNum 	= int(spl[0][1:])
		dataType 	= spl[1][:spl[1].index('(')]
		brackets 	= spl[1][spl[1].index('('):].strip()[0:-1]
		return IFCDataLine(ifcNum, dataType, brackets)
					
	def getLine(self, num):
		return self.dataList[num-1]
		

	
	
def parseColor(numLines):	
	pass
		

lines = getFileLines('301110FJK-Project-Final.ifc')
# ought to be data lines:
m = IFCLineManager(lines)
names = [px.brackets.split(',')[2] for px in m.BldElemProxys]
print ('\n'.join(names))
# for dl in m.dataList:
	# if dl != None:
		# print dl.dataType

# numLines= lines[7:-2]	
# dataLines = [parseDataLine(line) for line in numLines]
# dataList = [None] * dataLines[-1].ifcNum
# for dl in dataLines: dataList[int(dl.ifcDataNum)-1]=dl

