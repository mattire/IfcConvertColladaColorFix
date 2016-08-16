
import collada
import numpy as np
import xml.etree.ElementTree


class DaeEffectEditor(object):

    def __init__(self, 
                 fileName, 
                 lineManager,
                 ):
        self.mesh = collada.Collada(fileName)
        self.origDaeEffectIds = [e.id for e in self.mesh.effects]
        self.ifc = lineManager
        
        self.encodeColladaColors()
        self.createElementIdUpper2CamelMapping()
        # self.cheapFix()
        self.gen1Fix()
        

        # print 'saving smthng'
        fileName = 'out0.dae'
        with open(fileName,'w')as fp:
            self.mesh.write(fp)
        self.xmlHack(fileName)
    
    
            
    def xmlHack(self, fileName):
        tree = xml.etree.ElementTree.parse(fileName)
        r= tree.getroot()
        # geometries
        gs = r.findall('.//{http://www.collada.org/2005/11/COLLADASchema}geometry')
        geomDict= {int(g.attrib['id'][15:]):g for g in gs}
        igs =r.findall('.//{http://www.collada.org/2005/11/COLLADASchema}instance_geometry')
        igeomDict={int(g.attrib['url'][16:]):g for g in igs}
        
        for gk in geomDict.keys():
            tr = geomDict[gk].findall('.//{http://www.collada.org/2005/11/COLLADASchema}triangles')[0]
            mat = self.ifc.getElementNewMaterial(gk, tr.attrib['material'])
            #print (mat)
            if mat!=None:
                oldCamelMat = self.elementIdUpper2CamelMapping[tr.attrib['material'].upper()]
                camelMat = oldCamelMat + mat[len(oldCamelMat):]
                tr.attrib['material'] = camelMat
    
                # fix bindings
                imats = igeomDict[gk].findall('.//{http://www.collada.org/2005/11/COLLADASchema}instance_material')
                if len(imats)!=0:
                    #print ('*'), imats[0].attrib['symbol'], " ", imats[0].attrib['target'] , " ", camelMat
                    imats[0].attrib['symbol'] = camelMat
                    imats[0].attrib['target'] = '#' + camelMat
            
        tree.write(fileName)


            
    def createElementIdUpper2CamelMapping(self):
        self.camelIds = [ e.id for e in self.mesh.effects]
        self.elementIdUpper2CamelMapping = { id.upper()[:-3]:id[:-3] for id in self.camelIds }
    
    def cheapFix(self):
        for k in self.daeColors.keys():
            if k in self.elementIdUpper2CamelMapping: 
                key1 = self.daeColors[k].keys()[0]
                frstColor = self.daeColors[k][key1]
                daeFxId = self.elementIdUpper2CamelMapping[k]+'-fx'
                # print daeFxId
                # print frstColor
                self.mesh.effects[daeFxId].diffuse = frstColor    
                print (self.mesh.effects[daeFxId].diffuse)
                
    def gen1Fix(self):
        for k1 in self.daeColors.keys():
            if k1 in ['IFCPROJECT','IFCSITE','IFCBUILDING','IFCBUILDINGSTOREY','IFCOPENINGELEMENT']:
                continue
            oldfx = self.elementIdUpper2CamelMapping[k1]
            
            # add new effects and materials
            for ifxName in self.daeColors[k1]:
                eName = oldfx + ifxName[len(oldfx):] + '-fx'
                mName = oldfx + ifxName[len(oldfx):]
                # print self.daeColors[k1][mName.upper()]
                c = self.daeColors[k1][mName.upper()]
                if mName.upper().startswith('IFCWINDOW'):
                    print ('--*')
                    c = (c[0], c[1], c[2], c[3]*0.2)
                effect = None
                if mName.upper().startswith('IFCWINDOW'):
                    t = (0.8, 0.8, 0.8, 1.0)
                    tc = 0.7
                    effect = collada.material.Effect(eName, [], 'lambert', diffuse=c, ambient=c, transparent=t, transparency=tc ) #, specular=(0,1,0))
                else:
                    effect = collada.material.Effect(eName, [], 'lambert', diffuse=c, ambient=c) #, specular=(0,1,0))
                mat = collada.material.Material(mName, mName, effect)
                self.mesh.effects.append(effect)
                self.mesh.materials.append(mat)
                
                # self.mesh.scene.

            continue
            # go thru representations geometries and change new materials
            map = self.ifc.oldNewFxMap[k1]
            for k2 in map.keys():
                numStr = k2[len(k1):]
                matName = self.elementIdUpper2CamelMapping[k2[:len(k1)]]+numStr
                # print matName
                reps = map[k2][1]
                for r in reps:
                    repkey = 'representation-' + str(r)
                    # print repkey
                    gRepList =  [g for g in self.mesh.geometries if g.id == repkey]
                    if len(gRepList)!=0:
                        gRep = gRepList[0]
                        gRep.material = matName
                        gRep.bind(np.identity(3), matName)
        pass
    
                
    def effectiveRemapping(self):
        # find similar colors from different elems
        colorElems = []
        for k in self.ifc.oldNewFxMap.keys():
            pass
        pass
    
        
    def encodeColladaColors(self):
        newColor = lambda l: (float(l[0])/255, float(l[1])/255, float(l[2])/255, 1.0)
        self.daeColors = {}
        for k in self.ifc.oldNewFxMap.keys():
            list = self.ifc.oldNewFxMap[k]
            newSubColorMap = {k2: newColor(list[k2][0]) for k2 in list.keys()}
            self.daeColors[k] = newSubColorMap
        pass
