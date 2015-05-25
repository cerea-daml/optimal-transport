#############################
# Class PlottingConfiguration
#############################
#
# Defines everything necessary for plotting the result of an OT algorithm from a config file
#

from plotter     import Plotter

from ...utils.configuration.defaultConfiguration import DefaultConfiguration
from ...utils.io                                 import fileNameSuffix

class PlottingConfiguration(DefaultConfiguration):
    '''
    Stores the configuraion for plotting an OT algorithm
    '''

    def __init__(self, plottingConfigFile=None):
        DefaultConfiguration.__init__(self, plottingConfigFile)

    def __repr__(self):
        return 'PlottingConfiguration for a 1D OT algoritm'

    def plotter(self):
        return Plotter(self)

    def ckeckAttributes(self):
        DefaultConfiguration.ckeckAttributes(self)

        if self.singleOrMulti == 1:
            i    = len(self.label)
            iMax = len(self.outputDir)

            while i < iMax:
                self.label.append('sim'+fileNameSuffix(i, iMax))
                i += 1

    def defaultAttributes(self):
        DefaultConfiguration.defaultAttributes(self)

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
        self.defaultValues['extension']  = ['.pdf']
        self.isSubAttribute['extension'] = []
        self.isList['extension']         = True
        self.isDict['extension']         = False
        self.attributeType['extension']  = str

        self.attributes.append('outputDir')
        self.defaultValues['outputDir']  = ['./output/']
        self.isSubAttribute['outputDir'] = []
        self.isList['outputDir']         = True
        self.isDict['outputDir']         = False
        self.attributeType['outputDir']  = str

        self.attributes.append('label')
        self.defaultValues['label']  = ['sim0']
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

        self.attributes.append('plotFinalState')
        self.defaultValues['plotFinalState']  = 1
        self.isSubAttribute['plotFinalState'] = []
        self.isList['plotFinalState']         = False
        self.isDict['plotFinalState']         = False
        self.attributeType['plotFinalState']  = int

        self.attributes.append('prefixFigNameFinalState')
        self.defaultValues['prefixFigNameFinalState']  = 'finalState'
        self.isSubAttribute['prefixFigNameFinalState'] = []
        self.isList['prefixFigNameFinalState']         = False
        self.isDict['prefixFigNameFinalState']         = False
        self.attributeType['prefixFigNameFinalState']  = str

        self.attributes.append('transparencyFunctionName')
        self.defaultValues['transparencyFunctionName']  = 'customTransparency'
        self.isSubAttribute['transparencyFunctionName'] = []
        self.isList['transparencyFunctionName']         = False
        self.isDict['transparencyFunctionName']         = False
        self.attributeType['transparencyFunctionName']  = str

        self.attributes.append('plotFinalStatePlotter')
        self.defaultValues['plotFinalStatePlotter']  = 'imshow'
        self.isSubAttribute['plotFinalStatePlotter'] = []
        self.isList['plotFinalStatePlotter']         = False
        self.isDict['plotFinalStatePlotter']         = False
        self.attributeType['plotFinalStatePlotter']  = str

        self.attributes.append('plotFinalStateArgs')
        self.defaultValues['plotFinalStateArgs']  = None 
        self.isSubAttribute['plotFinalStateArgs'] = []
        self.isList['plotFinalStateArgs']         = False
        self.isDict['plotFinalStateArgs']         = True
        self.attributeType['plotFinalStateArgs']  = None

        self.attributes.append('plotFinalStateArgsInit')
        self.defaultValues['plotFinalStateArgsInit']  = None
        self.isSubAttribute['plotFinalStateArgsInit'] = []
        self.isList['plotFinalStateArgsInit']         = False
        self.isDict['plotFinalStateArgsInit']         = True
        self.attributeType['plotFinalStateArgsInit']  = None
