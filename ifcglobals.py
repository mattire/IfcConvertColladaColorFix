byPassList =['IFCPROJECT','IFCSITE','IFCBUILDING','IFCBUILDINGSTOREY','None']

representationBranchPath = [[   ('IFCBUILDINGELEMENTPROXY',None),\
                                ('IFCCOVERING',None),\
                                ('IFCBEAM',None),\
                                ('IFCCOLUMN',None),\
                                ('IFCCURTAINWALL',None),\
                                ('IFCDOOR',None),\
                                ('IFCMEMBER',None),\
                                ('IFCPLATE',None),\
                                ('IFCRAILING',None),\
                                ('IFCRAMP',None),\
                                ('IFCRAMPFLIGHT',None),\
                                ('IFCROOF',None),\
                                ('IFCSLAB',None),\
                                ('IFCSTAIR',None),\
                                ('IFCSTAIRFLIGHT',None),\
                                ('IFCWALL',None),\
                                ('IFCWINDOW',None),\
                                ('IFCBUILDINGELEMENTCOMPONENT',None),\
                                ('IFCFOOTING',None),\
                                ('IFCPILE',None),\
                                ('IFCFURNISHINGELEMENT', None),\
                                ('IFCFLOWTERMINAL', None),\
                                ('IFCTRANSPORTELEMENT', None),\
                                ('IFCWALLSTANDARDCASE', None)], \
                                ('IFCPRODUCTDEFINITIONSHAPE', None),\
                                ('IFCSHAPEREPRESENTATION', None)]  # can have multiple IFCSHAPEREPRESENTATION presentations
                                                                    # bounding boxes should be ignored
colorRootPath = [ ('IFCPROPERTYSET',None) ,\
                    ('IFCCOMPLEXPROPERTY','Color'),
                    [ ('IFCPROPERTYSINGLEVALUE','Red'),\
                    ('IFCPROPERTYSINGLEVALUE','Green'),\
                    ('IFCPROPERTYSINGLEVALUE','Blue')]\
                ]

#globalPathLists = [representationBranchPath, colorRootPath]
#interestingNodes = []
#for gpl in globalPathLists:
#    for elem in gpl:
#        if type(elem) is list: 
#            interestingNodes.extend([i[0] for i in elem])
#        else:
#            interestingNodes.append(elem[0])
#interestingNodes = list(set(interestingNodes))

#print interestingNodes
#import sys
#sys.exit()

interestingNodes = ['IFCRELDEFINESBYPROPERTIES',\
                    'IFCFURNISHINGELEMENT',\
                    'IFCWALLSTANDARDCASE',\
                    'IFCTRANSPORTELEMENT',\
                    'IFCFLOWTERMINAL',\
                    'IFCBUILDINGELEMENTPROXY', \
                    'IFCCOVERING', \
                    'IFCBEAM', \
                    'IFCCOLUMN', \
                    'IFCCURTAINWALL', \
                    'IFCDOOR', \
                    'IFCMEMBER', \
                    'IFCPLATE', \
                    'IFCRAILING', \
                    'IFCRAMP', \
                    'IFCRAMPFLIGHT', \
                    'IFCROOF', \
                    'IFCSLAB', \
                    'IFCSTAIR', \
                    'IFCSTAIRFLIGHT', \
                    'IFCWALL', \
                    'IFCWINDOW', \
                    'IFCBUILDINGELEMENTCOMPONENT', \
                    'IFCFOOTING', \
                    'IFCPILE', \
                    'IFCPRODUCTDEFINITIONSHAPE', \
                    'IFCSHAPEREPRESENTATION', \
                    'IFCPROPERTYSET', \
                    'IFCCOMPLEXPROPERTY', \
                    'IFCPROPERTYSINGLEVALUE', \
                    'IFCPROPERTYSINGLEVALUE', \
                    'IFCPROPERTYSINGLEVALUE']

