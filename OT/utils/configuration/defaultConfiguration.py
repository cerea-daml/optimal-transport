#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#________________________
# defaultConfiguration.py
#________________________

from ..io.io        import readLines
from ..types.cast   import castString
from ..types.string import catListOfString

#__________________________________________________

class DefaultConfiguration(object):

    def __init__(self, configFile=None):
        self.defaultAttributes()
        self.initListsAndDicts()
        self.fromfile(configFile)
        self.checkAttributes()

    #_________________________

    def __repr__(self):
        return 'DefaultConfiguration class'
        
    #_________________________

    def replaceByDefaultValue(self, attr):
        self.__setattr__(attr, self.defaultValues[attr])
        if self.printWarning[attr]:
            print('No valid element found for '+attr)
            print('Replaced by default value : ')
            print(self.defaultValues[attr])

    #_________________________

    def checkAttribute(self, attr):
        if self.attributeType[attr] == 'dict':
            if self.__getattribute__(attr) == {}:
                self.replaceByDefaultValue(attr)
        elif self.attributeType[attr] == 'list':
            if self.__getattribute__(attr) == []:
                self.replaceByDefaultValue(attr)
        else:
            if not self.__dict__.has_key(attr):
                self.replaceByDefaultValue(attr)
    
    #_________________________

    def checkAttributes(self):
        for attr in self.attributes:
            if self.isSubAttribute[attr] == []:
                self.checkAttribute(attr)

        for attr in self.attributes:
            if len(self.isSubAttribute[attr]) > 0:
                parentAttributesCompatible = True
                for (parentAttr, parentValue) in self.isSubAttribute[attr]:
                    if not self.__getattribute__(parentAttr) == parentValue:
                        parentAttributesCompatible = False
                        break
                if parentAttributesCompatible:
                    self.checkAttribute(attr)

    #_________________________

    def fromfile(self, fileName):
        lines = readLines(fileName, strip=True, removeBlancks=True, commentChar='#', includeEmptyLines=False)

        for line in lines:
            try:
                members   = line.split('=')
                attrName  = members.pop(0)
                attrValue = catListOfString(members)

                if not attrValue == '' and attrName in self.attributes:
                    
                    if self.attributeType[attrName] == 'dict':
                        members = attrValue.split(':')
                        key     = members.pop(0)
                        if '&None&' in catListOfString(members):
                            value = None
                        else:
                            value = castString(members.pop(0), catListOfString(members))
                        self.__getattribute__(attrName)[key] = value

                    elif self.attributeType[attrName] == 'list':
                        members = attrValue.split(':')
                        self.__getattribute__(attrName).append(castString(members.pop(0), catListOfString(members)))

                    else:
                        self.__setattr__(attrName, castString(self.attributeType[attrName], attrValue))
            except:
                print('Could not read line : '+line)

    #_________________________

    def initListsAndDicts(self):
        for attr in self.attributes:
            if self.attributeType[attr] == 'list':                
                self.__setattr__(attr, [])
            elif self.attributeType[attr] == 'dict':
                self.__setattr__(attr, {})

    #_________________________

    def defaultAttributes(self):
        self.attributes     = []
        self.defaultValues  = {}
        self.isSubAttribute = {}
        self.attributeType  = {}
        self.printWarning   = {}

    #_________________________

    def addAttribute(self, attrName, defaultVal=None, isSubAttr=[], attrType='str', printWarning=True):
        self.attributes.append(attrName)
        self.defaultValues[attrName]  = defaultVal
        self.isSubAttribute[attrName] = isSubAttr
        self.attributeType[attrName]  = attrType
        self.printWarning[attrName]   = printWarning

    #_________________________

    def writeConfig(self, fileName):
        def writeElement(f, e):
            if isinstance(e, str):
                f.write(' str : '+e+'\n')
            elif isinstance(e, int):
                f.write(' int : '+str(e)+'\n')
            elif isinstance(e, float):
                f.write(' float : '+str(e)+'\n')
            elif isinstance(e, bool):
                f.write(' bool : '+str(e)+'\n')

        f = open(fileName, 'w')
        f.write('#'+self.__repr__()+'\n')

        for attr in self.attributes:
            try:
                attrType = self.attributeType[attr]

                if attrType == 'list':
                    l = self.__getattribute__(attr)

                    for e in l:
                        f.write(attr+' =')
                        writeElement(f, e)

                elif attrType == 'dict':
                    d = self.__getattribute__(attr)
                    
                    for key in d:
                        e = d[key]
                        f.write(attr+' = '+key+' :')
                        writeElement(f, e)

                else:
                    f.write(attr+' = '+str(self.__getattribute__(attr))+'\n')

            except:
                pass

        f.close()

    #_________________________

    def printConfig(self):
        def printElement(e):
            if isinstance(e, str):
                return (' str : '+e)
            elif isinstance(e, int):
                return (' int : '+str(e))
            elif isinstance(e, float):
                return (' float : '+str(e))
            elif isinstance(e, bool):
                return (' bool : '+str(e))

        for attr in self.attributes:
            try:
                attrType = self.attributeType[attr]

                if attrType == 'list':
                    l = self.__getattribute__(attr)

                    for e in l:
                        print(attr+' ='+printElement(e))

                elif attrType == 'dict':
                    d = self.__getattribute__(attr)

                    for key in d:
                        e = d[key]
                        print(attr+' = '+key+' :'+printElement(e))
        
                else:
                    print(attr+' = '+str(self.__getattribute__(attr)))

            except:
                pass
#__________________________________________________
