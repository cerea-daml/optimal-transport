#############################
# Class PlottingConfiguration
#############################
#
# Defines everything necessary for plotting the result of an OT algorithm from a config file
#

from plotter     import Plotter

from ...utils.io import fileNameSuffix

class PlottingConfiguration(object):
    '''
    Stores the configuraion for an OT algorithm
    '''

    def __init__(self, plottingConfigFile=None):
        self.defaultAttributes()
        self.initListsAndDicts()
        self.fromfile(plottingConfigFile)
        self.ckeckAttributes()

    def __repr__(self):
        return 'PlottingConfiguration for a 1D OT algoritm'

    def plotter(self):
        return Plotter(self)

    def ckeckAttributes(self):
        for attr in self.attributes:
            if self.isSubAttribute[attr] == [] and not self.isDict[attr]:
                if self.isList[attr]:
                    if self.__getattribute__(attr) == [] and self.defaultValues[attr] is not None:
                        print('No valid element found for list '+attr+' .')
                        print('Filling by 1 default value : '+str(self.defaultValues[attr])+' .')
                        self.__setattr__(attr, [self.defaultValues[attr]])
                elif not self.__dict__.has_key(attr):
                    print('No valid value found for parameter '+attr'.')
                    print('Replacing by default value '+str(self.defaultValues[attr])+' .')
                    self.__setattr(attr, self.defaultValues[attr])

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
                            print('Filling by 1 default value : '+str(self.defaultValues[attr])+' .')
                            self.__setattr__(attr, [self.defaultValues[attr]])
                    elif not self.__dict__.has_key(attr):
                        print('No valid value found for parameter '+attr'.')
                        print('Replacing by default value '+str(self.defaultValues[attr])+' .')
                        self.__setattr(attr, self.defaultValues[attr])

        if self.singleOrMulti == 1:
            i    = len(self.label)
            iMax = len(self.outputDir)

            while i < iMax:
                self.label.append('sim'+fileNameSuffix(i, iMax))
                i += 1

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
                l = line.split('=')
                attrName = l[0]
                attrValue = l[1]

                for attr in self.attributes:
                    if attrName == attr:
                        if self.isList[attr]:
                            self.__getattribute__(attr).append(self.attributeType[attr](attrValue))
                        elif self.isDict[attr]:
                            val = attrValue.split(':')
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
                pass

    def initListsAndDicts(self):
        for attr in self.attributes:
            if self.isList[attr] == True:
                self.__setattr__(attr, [])
            elif self.isDict[attr] == True:
                self.__setattr__(attr, {})

    def defaultAttributes(self):
        self.attributes     = []
        self.defaultValues  = {}
        self.isSubAttribute = {}
        self.isList         = {}
        self.isDict         = {}
        self.attributeType  = {}

        self.attributes.append('EPSILON')
        self.defaultValues['EPSILON']  = 1.e-8
        self.isSubAttribute['EPSILON'] = []
        self.isList['EPSILON']         = False
        self.isDict['EPSILON']         = False
        self.attributeType['EPSILON']  = float

        self.attributes.append('singleOrMulti')
        self.defaultValues['singleOrMulti']  = 0
        self.isSubAttribute['singleOrMulti'] = []
        self.isList['singleOrMulti']         = False
        self.isDict['singleOrMulti']         = False
        self.attributeType['singleOrMulti']  = int

        self.attributes.append('figDir')
        self.defaultValues['figDir']  = './figures/'
        self.isSubAttribute['figDir'] = []
        self.isList['figDir']         = False
        self.isDict['figDir']         = False
        self.attributeType['figDir']  = str

        self.attributes.append('extension')
        self.defaultValues['extension']  = '.pdf'
        self.isSubAttribute['extension'] = []
        self.isList['extension']         = True
        self.isDict['extension']         = False
        self.attributeType['extension']  = str

        self.attributes.append('outputDir')
        self.defaultValues['outputDir']  = './output/'
        self.isSubAttribute['outputDir'] = []
        self.isList['outputDir']         = True
        self.isDict['outputDir']         = False
        self.attributeType['outputDir']  = str

        self.attributes.append('label')
        self.defaultValues['label']  = ''
        self.isSubAttribute['label'] = []
        self.isList['label']         = True
        self.isDict['label']         = False
        self.attributeType['label']  = str

        self.attributes.append('plotAnalyse')
        self.defaultValues['plotAnalyse']  = 1 
        self.isSubAttribute['plotAnalyse'] = []
        self.isList['plotAnalyse']         = False
        self.isDict['plotAnalyse']         = False
        self.attributeType['plotAnalyse']  = int

        self.attributes.append('plotSubplotsFunctionName')
        self.defaultValues['plotSubplotsFunctionName']  = 'customPlotSubplots' 
        self.isSubAttribute['plotSubplotsFunctionName'] = [('plotAnalyse', 1)]
        self.isList['plotSubplotsFunctionName']         = False
        self.isDict['plotSubplotsFunctionName']         = False
        self.attributeType['plotSubplotsFunctionName']  = str

        self.attributes.append('prefixFigNameAnalyse')
        self.defaultValues['prefixFigNameAnalyse']  = 'analyse' 
        self.isSubAttribute['prefixFigNameAnalyse'] = [('plotAnalyse', 1)]
        self.isList['prefixFigNameAnalyse']         = False
        self.isDict['prefixFigNameAnalyse']         = False
        self.attributeType['prefixFigNameAnalyse']  = str

        self.attributes.append('plotSubplotsFunctionArgs')
        self.defaultValues['plotSubplotsFunctionArgs']  = None
        self.isSubAttribute['plotSubplotsFunctionArgs'] = [('plotAnalyse', 1)]
        self.isList['plotSubplotsFunctionArgs']         = False
        self.isDict['plotSubplotsFunctionArgs']         = True
        self.attributeType['plotSubplotsFunctionArgs']  = None
