#############################
# Class PlottingConfiguration
#############################
#
# Defines everything necessary for plotting the result of an OT algorithm from a config file
#

from plotter import Plotter

from ...utils.io.io                              import fileNameSuffix
from ...utils.configuration.defaultConfiguration import DefaultConfiguration

class PlottingConfiguration(DefaultConfiguration):
    '''
    Stores the configuraion for plotting a 1D OT algorithm
    '''

    def __init__(self, plottingConfigFile=None):
        DefaultConfiguration.__init__(self, plottingConfigFile)

    def __repr__(self):
        return 'PlottingConfiguration for a 1D OT algoritm'

    def plotter(self):
        return Plotter(self)

    def checkAttributes(self):
        DefaultConfiguration.checkAttributes(self)

        if self.singleOrMulti == 1:
            i    = len(self.label)
            iMax = len(self.outputDir)

            while i < iMax:
                self.label.append('sim'+fileNameSuffix(i, iMax))
                i += 1

    def defaultAttributes(self):
        DefaultConfiguration.defaultAttributes(self)

        self.attributes.append('EPSILON')
        self.defaultValues['EPSILON']                   = 1.e-8
        self.isSubAttribute['EPSILON']                  = []
        self.isList['EPSILON']                          = False
        self.isDict['EPSILON']                          = False
        self.attributeType['EPSILON']                   = float

        self.attributes.append('singleOrMulti')
        self.defaultValues['singleOrMulti']             = 0
        self.isSubAttribute['singleOrMulti']            = []
        self.isList['singleOrMulti']                    = False
        self.isDict['singleOrMulti']                    = False
        self.attributeType['singleOrMulti']             = int

        self.attributes.append('figDir')
        self.defaultValues['figDir']                    = './figures/'
        self.isSubAttribute['figDir']                   = []
        self.isList['figDir']                           = False
        self.isDict['figDir']                           = False
        self.attributeType['figDir']                    = str

        self.attributes.append('extension')
        self.defaultValues['extension']                 = ['.pdf']
        self.isSubAttribute['extension']                = []
        self.isList['extension']                        = True
        self.isDict['extension']                        = False
        self.attributeType['extension']                 = str

        self.attributes.append('outputDir')
        self.defaultValues['outputDir']                 = ['./output/']
        self.isSubAttribute['outputDir']                = []
        self.isList['outputDir']                        = True
        self.isDict['outputDir']                        = False
        self.attributeType['outputDir']                 = str

        self.attributes.append('label')
        self.defaultValues['label']                     = ['sim0']
        self.isSubAttribute['label']                    = []
        self.isList['label']                            = True
        self.isDict['label']                            = False
        self.attributeType['label']                     = str

        self.attributes.append('plotAnalyse')
        self.defaultValues['plotAnalyse']               = 1 
        self.isSubAttribute['plotAnalyse']              = []
        self.isList['plotAnalyse']                      = False
        self.isDict['plotAnalyse']                      = False
        self.attributeType['plotAnalyse']               = int

        self.attributes.append('plotSubplotsFunctionName')
        self.defaultValues['plotSubplotsFunctionName']  = 'customPlotSubplots' 
        self.isSubAttribute['plotSubplotsFunctionName'] = [('plotAnalyse', 1)]
        self.isList['plotSubplotsFunctionName']         = False
        self.isDict['plotSubplotsFunctionName']         = False
        self.attributeType['plotSubplotsFunctionName']  = str

        self.attributes.append('prefixFigNameAnalyse')
        self.defaultValues['prefixFigNameAnalyse']      = 'analyse' 
        self.isSubAttribute['prefixFigNameAnalyse']     = [('plotAnalyse', 1)]
        self.isList['prefixFigNameAnalyse']             = False
        self.isDict['prefixFigNameAnalyse']             = False
        self.attributeType['prefixFigNameAnalyse']      = str

        self.attributes.append('plotSubplotsFunctionArgs')
        self.defaultValues['plotSubplotsFunctionArgs']  = None
        self.isSubAttribute['plotSubplotsFunctionArgs'] = [('plotAnalyse', 1)]
        self.isList['plotSubplotsFunctionArgs']         = False
        self.isDict['plotSubplotsFunctionArgs']         = True
        self.attributeType['plotSubplotsFunctionArgs']  = None

        self.attributes.append('plotFinalState')
        self.defaultValues['plotFinalState']            = 1
        self.isSubAttribute['plotFinalState']           = []
        self.isList['plotFinalState']                   = False
        self.isDict['plotFinalState']                   = False
        self.attributeType['plotFinalState']            = int

        self.attributes.append('plotFinalState_prefixFigName')
        self.defaultValues['plotFinalState_prefixFigName']         = 'finalState'
        self.isSubAttribute['plotFinalState_prefixFigName']        = [('plotFinalState',1)]
        self.isList['plotFinalState_prefixFigName']                = False
        self.isDict['plotFinalState_prefixFigName']                = False
        self.attributeType['plotFinalState_prefixFigName']         = str

        self.attributes.append('plotFinalState_transparencyFunction')
        self.defaultValues['plotFinalState_transparencyFunction']  = 'customTransparency'
        self.isSubAttribute['plotFinalState_transparencyFunction'] = [('plotFinalState',1)]
        self.isList['plotFinalState_transparencyFunction']         = False
        self.isDict['plotFinalState_transparencyFunction']         = False
        self.attributeType['plotFinalState_transparencyFunction']  = str

        self.attributes.append('plotFinalState_addLegend')
        self.defaultValues['plotFinalState_addLegend']             = 1
        self.isSubAttribute['plotFinalState_addLegend']            = [('plotFinalState',1)]
        self.isList['plotFinalState_addLegend']                    = False
        self.isDict['plotFinalState_addLegend']                    = False
        self.attributeType['plotFinalState_addLegend']             = int

        self.attributes.append('plotFinalState_grid')
        self.defaultValues['plotFinalState_grid']                  = 1
        self.isSubAttribute['plotFinalState_grid']                 = [('plotFinalState',1)]
        self.isList['plotFinalState_grid']                         = False
        self.isDict['plotFinalState_grid']                         = False
        self.attributeType['plotFinalState_grid']                  = int

        self.attributes.append('plotFinalState_addTimeTextPbar')
        self.defaultValues['plotFinalState_addTimeTextPbar']       = 1
        self.isSubAttribute['plotFinalState_addTimeTextPbar']      = [('plotFinalState',1)]
        self.isList['plotFinalState_addTimeTextPbar']              = False
        self.isDict['plotFinalState_addTimeTextPbar']              = False
        self.attributeType['plotFinalState_addTimeTextPbar']       = int

        self.attributes.append('plotFinalState_xLabel')
        self.defaultValues['plotFinalState_xLabel']                = None
        self.isSubAttribute['plotFinalState_xLabel']               = [('plotFinalState',1)]
        self.isList['plotFinalState_xLabel']                       = False
        self.isDict['plotFinalState_xLabel']                       = False
        self.attributeType['plotFinalState_xLabel']                = str

        self.attributes.append('plotFinalState_yLabel')
        self.defaultValues['plotFinalState_yLabel']                = None
        self.isSubAttribute['plotFinalState_yLabel']               = [('plotFinalState',1)]
        self.isList['plotFinalState_yLabel']                       = False
        self.isDict['plotFinalState_yLabel']                       = False
        self.attributeType['plotFinalState_yLabel']                = str

        self.attributes.append('plotFinalState_nbrXTicks')
        self.defaultValues['plotFinalState_nbrXTicks']             = 3
        self.isSubAttribute['plotFinalState_nbrXTicks']            = [('plotFinalState',1)]
        self.isList['plotFinalState_nbrXTicks']                    = False
        self.isDict['plotFinalState_nbrXTicks']                    = False
        self.attributeType['plotFinalState_nbrXTicks']             = int

        self.attributes.append('plotFinalState_nbrYTicks')
        self.defaultValues['plotFinalState_nbrYTicks']             = 3
        self.isSubAttribute['plotFinalState_nbrYTicks']            = [('plotFinalState',1)]
        self.isList['plotFinalState_nbrYTicks']                    = False
        self.isDict['plotFinalState_nbrYTicks']                    = False
        self.attributeType['plotFinalState_nbrYTicks']             = int

        self.attributes.append('plotFinalState_xTicksRound')
        self.defaultValues['plotFinalState_xTicksRound']           = 1
        self.isSubAttribute['plotFinalState_xTicksRound']          = [('plotFinalState',1)]
        self.isList['plotFinalState_xTicksRound']                  = False
        self.isDict['plotFinalState_xTicksRound']                  = False
        self.attributeType['plotFinalState_xTicksRound']           = int

        self.attributes.append('plotFinalState_yTicksRound')
        self.defaultValues['plotFinalState_yTicksRound']           = 1
        self.isSubAttribute['plotFinalState_yTicksRound']          = [('plotFinalState',1)]
        self.isList['plotFinalState_yTicksRound']                  = False
        self.isDict['plotFinalState_yTicksRound']                  = False
        self.attributeType['plotFinalState_yTicksRound']           = int
