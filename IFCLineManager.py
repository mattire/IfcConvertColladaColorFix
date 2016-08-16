
import sys


byPassList =['IFCPROJECT','IFCSITE','IFCBUILDING','IFCBUILDINGSTOREY']

def stripBrackets(content):
	start = content.find('(')+1
	end = content.rfind(')')
	return content[start:end]
	

class IFCDataLine:
	def __init__(self, dn, type, brackets):
		self.ifcNum = dn
		self.dataType = type
		self.brackets = brackets
		
	def printSelf(self):
		for k in self.__dict__.keys(): print (self.__dict__[k])
		
class IFCSingleValue:
	def __init__(self, dataLine):
		spl = stripBrackets(dataLine.brackets).split(',')[0]
		self.name = spl[0]
		ifcValue = spl[2]
		
class IFCPropertySet:
	def __init__(self, dataLine, manager):
		# print dataLine.dataType
		# dataLine.printSelf()
		t = eval(dataLine.brackets.replace('#','').replace('$','""'))
		# print t
		self.label 		= t[4][0]
		self.complex 	= t[4][1]
		DLComplex = manager.dataList[self.complex]
		
		if eval(DLComplex.brackets.replace('#','').replace('$','""'))[0]=='Color':
			rgbAddresses = eval(DLComplex.brackets.replace('#','').replace('$','""'))[3]
			DLred	= manager.dataList[rgbAddresses[0]]
			DLgreen	= manager.dataList[rgbAddresses[1]]
			DLblue	= manager.dataList[rgbAddresses[2]]
			r=eval(DLred	.brackets.replace('#','').replace('$','""').replace('IFCINTEGER','int'))[2]
			g=eval(DLgreen	.brackets.replace('#','').replace('$','""').replace('IFCINTEGER','int'))[2]
			b=eval(DLblue	.brackets.replace('#','').replace('$','""').replace('IFCINTEGER','int'))[2]
			self.rgb = (r,g,b)

class IFCShapePresentation(object):
	def __init__(self, dataLine, manager):
		pass
	def m1(self):
		pass

			
class IFCRelation:
	def __init__(self, dataLine, manager):
		manager 				= manager
		self.parentPtr 			= int(stripBrackets(stripBrackets(dataLine.brackets).split(',')[4])[1:])
		self.propertySetPtr 	= int(stripBrackets(dataLine.brackets).split(',')[5][1:])
		
		self.DLParent			= manager.dataList[self.parentPtr]
		if self.DLParent.dataType not in ['IFCPROJECT','IFCSITE','IFCBUILDING','IFCBUILDINGSTOREY']:
			# print self.DLParent.dataType
			# print self.DLParent.brackets
			# print stripBrackets(self.DLParent.brackets).split(',')[6][1:]
			productDefShapePtr 		= int(stripBrackets(self.DLParent.brackets).split(',')[6][1:])
			self.DLProductDefShape 	= manager.dataList[productDefShapePtr]
			
			self.prodPresentationPtr= eval(self.DLProductDefShape.brackets.replace('#','').replace('$','""'))[2][0]
			
		else:
			self.prodPresentationPtr=0
			
		self.DLPropertySet	= manager.dataList[self.propertySetPtr]
		
		self.PropSet 	= IFCPropertySet(self.DLPropertySet, manager)		
		
		
class IFCLineManager:

	def __init__(self, fName):
		lines = None
		with open(fName) as ifcFile:
			lines = ifcFile.readlines()
		numLines= lines[7:-2]		
		self.dataLines = [self.parseDataLine(line) for line in numLines]
		
		# data list: all the data lines (IFCDataLine) organized
		self.dataList = [None] * (self.dataLines[-1].ifcNum + 1)
		for dl in self.dataLines: self.dataList[dl.ifcNum]=dl		
		self.initRelations()
		self.createRelationColorTables()
		self.createNewFXNames()

	def getElementNewMaterial(self, elemId, oldType):
		newTypes = self.oldNewFxMap[oldType.upper()].keys()
		for nt in newTypes:
			tup = self.oldNewFxMap[oldType.upper()][nt.upper()]
			if elemId in tup[1]:
				return nt
		return None
		
		
	def initRelations(self):
		self.relLines 	= [line for line in self.dataLines if line.dataType=='IFCRELDEFINESBYPROPERTIES']
		self.relations 	= [IFCRelation(rl,self) for rl in self.relLines]
		
	def createRelationColorTables(self):
		dataTypes 					= list(set([ r.DLParent.dataType for r in self.relations]))
		self.dataTypesColorTuples	= [(r.DLParent.dataType, r.PropSet.rgb, r.prodPresentationPtr) \
										for r in self.relations]
		lt = self.dataTypesColorTuples
		types = set([t[0] for t in lt])
		colors= set([t[1] for t in lt])
		elems = set([t[2] for t in lt])
		f1 = lambda x : list(set(x))
		self.elemsWithColor = { c:[t[2] for t in lt if t[1]==c ] for c in colors }
		self.typesWithColor = { c:list(set([t[0] for t in lt if t[1]==c ])) for c in colors }
		self.colorsWithType = { tp:f1([t[1] for t in lt if t[0]==tp ]) for tp in types }
		self.elemsWithType	= { tp:f1([t[2] for t in lt if t[0]==tp ]) for tp in types }
		self.elemColor 		= { e: [t[1] for t in lt if t[2]==e][0] for e in elems if e !=0}
		
	def newFxTypeElemMap(self, ifcType):
		typePresentations = self.elemsWithType[ifcType]
		# print  '-----'
		# print ifcType
		# print typePresentations
		# print  '-----'
		
		newFxColorMap = {}
		
		for i in range(0,len(self.colorsWithType[ifcType])):
			colors = self.colorsWithType[ifcType]
			id_color_list = { ifcType + str(i): colors[i] for i in range(0,len(colors))}
			rep_color_list = {rep: self.elemColor[rep] for rep in typePresentations}
			# print id_color_list
			# print rep_color_list
			
			for id in id_color_list.keys():
				id_color = id_color_list[id]
				color_reps = [rep for rep in rep_color_list.keys() if rep_color_list[rep]==id_color]
				newFxColorMap[id]=(id_color, color_reps)
			
		# sys.exit()
		return newFxColorMap
		
	def createNewFXNames(self):
		self.oldNewFxMap = {}
		print (self.colorsWithType.keys())
		for ifcType in self.colorsWithType.keys():
			if ifcType in byPassList:
				continue
			map = self.newFxTypeElemMap(ifcType)
			self.oldNewFxMap[ifcType]=map	
		
	def parseDataLine(self, line):
		spl = line.split('=')
		ifcNum 	= int(spl[0][1:])
		dataType 	= spl[1][:spl[1].index('(')]
		brackets 	= spl[1][spl[1].index('('):].strip()[0:-1]
		return IFCDataLine(ifcNum, dataType, brackets)
					
	def getTypesLines(self, typeList):
		return {t:self.getTypeElementLines(t) for t in typeList}
					
	def getTypeElementLines(self, type):
		return [dl for dl in self.dataLines if dl.dataType==type]
				
	def getLine(self, num):
		return self.dataList[num-1]
