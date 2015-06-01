#########################
# defaultConfiguration.py
#########################

from ..io.io import readLines

def catListOfString(l):
    res = ''
    for s in l:
        res += s
    return res

def cast(toType, s):
    if toType == 'str':
        return s
    elif toType == 'float':
        return float(s)
    elif toType == 'int':
        return int(s)
    elif toType == 'bool':
        return ( s == 'True' )

class DefaultConfiguration(object):

    def __init__(self, configFile=None):
        self.defaultAttributes()
        self.initListsAndDicts()
        self.fromfile(configFile)
        self.checkAttributes()

    def __repr__(self):
        return 'DefaultConfiguration class'

    def replaceByDefaultValue(self, attr):
        self.__setattr__(attr, self.defaultValues[attr])
        if self.printWarning[attr]:
            print('No valid element found for '+attr)
            print('Replaced by default value : ')
            print(self.defaultValues[attr])

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

    def fromfile(self, fileName):
        lines = readLines(fileName, strip=True, removeBlancks=True, commentChar='#', includeEmptyLines=False)

        for line in lines:
            try:
            #if True:
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
                            value = cast(members.pop(0), catListOfString(members))
                        self.__getattribute__(attrName)[key] = value

                    elif self.attributeType[attrName] == 'list':
                        members = attrValue.split(':')
                        self.__getattribute__(attrName).append(cast(members.pop(0), catListOfString(members)))

                    else:
                        self.__setattr__(attrName, cast(self.attributeType[attrName], attrValue))
            except:
                print('Could not read line :'+line)

    def initListsAndDicts(self):
        for attr in self.attributes:
            if self.attributeType[attr] == 'list':                
                self.__setattr__(attr, [])
            elif self.attributeType[attr] == 'dict':
                self.__setattr__(attr, {})

    def defaultAttributes(self):
        self.attributes     = []
        self.defaultValues  = {}
        self.isSubAttribute = {}
        self.attributeType  = {}
        self.printWarning   = {}

    def addAttribute(self, attrName, defaultVal, isSubAttr, attrType, printWarning):
        self.attributes.append(attrName)
        self.defaultValues[attrName]  = defaultVal
        self.isSubAttribute[attrName] = isSubAttr
        self.attributeType[attrName]  = attrType
        self.printWarning[attrName]   = printWarning
