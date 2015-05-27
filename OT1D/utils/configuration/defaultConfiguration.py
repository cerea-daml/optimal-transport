#########################
# defaultConfiguration.py
#########################

class DefaultConfiguration(object):

    def __init__(self, configFile=None):
        self.defaultAttributes()
        self.initListsAndDicts()
        self.fromfile(configFile)
        self.checkAttributes()

    def __repr__(self):
        return 'DefaultConfiguration class'

    def checkAttributes(self):
        for attr in self.attributes:
            if self.isSubAttribute[attr] == [] and not self.isDict[attr]:
                if self.isList[attr]:
                    if self.__getattribute__(attr) == []:
                        print('No valid element found for list '+attr+' .')
                        print('Filling by default value : '+str(self.defaultValues[attr])+' .')
                        self.__setattr__(attr, self.defaultValues[attr])
                elif not self.__dict__.has_key(attr):
                    print('No valid value found for parameter '+attr+'.')
                    print('Replacing by default value : '+str(self.defaultValues[attr])+' .')
                    self.__setattr__(attr, self.defaultValues[attr])

        for attr in self.attributes:
            if len(self.isSubAttribute[attr]) > 0 and not self.isDict[attr]:
                parentAttributesCompatible = True
                for (parentAttr, parentValue) in self.isSubAttribute[attr]:
                    if not self.__getattribute__(parentAttr) == parentValue:
                        parentAttributesCompatible = False
                        break
                if parentAttributesCompatible:

                    if self.isList[attr]:
                        if self.__getattribute__(attr) == [] and self.defaultValues[attr] is not None:
                            print('No valid element found for list '+attr+' .')
                            print('Filling by default value : '+str(self.defaultValues[attr])+' .')
                            self.__setattr__(attr, self.defaultValues[attr])
                    elif not self.__dict__.has_key(attr):
                        print('No valid value found for parameter '+attr+'.')
                        print('Replacing by default value : '+str(self.defaultValues[attr])+' .')
                        self.__setattr__(attr, self.defaultValues[attr])

    def fromfile(self, fileName):
        try:
            f = open(fileName,'r')
            lines = f.readlines()
            f.close()
        except:
            return

        filteredLines = []
        for line in lines:
            l = line.strip().replace(' ','').split('#')[0]
            if not l == '':
                filteredLines.append(l)

        for line in filteredLines:
            try:
                l         = line.split('=')
                attrName  = l[0]
                attrValue = l[1]

                if not attrValue == '':
                    for attr in self.attributes:
                        if attrName == attr:
                            if self.isList[attr]:
                                self.__getattribute__(attr).append(self.attributeType[attr](attrValue))
                            elif self.isDict[attr]:
                                val   = attrValue.split(':')
                                value = val[2]
                                if val[1] == 'int':
                                    value = int(value)
                                elif val[1] == 'float':
                                    value = float(value)
                                elif val[1] == 'bool':
                                    value = ( value == 'True' )

                                self.__getattribute__(attr)[val[0]] = value
                            else:
                                self.__setattr__(attr, self.attributeType[attr](attrValue))
            except:
                print('Could not interpret line :')
                print(line)

    def initListsAndDicts(self):
        for attr in self.attributes:
            if self.isList[attr]:
                self.__setattr__(attr, [])
            elif self.isDict[attr]:
                self.__setattr__(attr, {})

    def defaultAttributes(self):
        self.attributes     = []
        self.defaultValues  = {}
        self.isSubAttribute = {}
        self.isList         = {}
        self.isDict         = {}
        self.attributeType  = {}

