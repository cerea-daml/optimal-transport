#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#____________________________
# Class PlottingConfiguration
#____________________________
#
# Defines everything necessary for plotting the result of an OT algorithm from a config file
#

from plotter                                     import Plotter
from ...utils.io.io                              import fileNameSuffix
from ...utils.configuration.defaultConfiguration import DefaultConfiguration

#__________________________________________________

class PlottingConfiguration(DefaultConfiguration):

    def __init__(self, plottingConfigFile=None):
        DefaultConfiguration.__init__(self, plottingConfigFile)

        i    = len(self.labelList)
        iMax = len(self.outputDirList)

        while i < iMax:
            self.labelList.append('sim'+fileNameSuffix(i, iMax))
            i += 1

    #_________________________

    def __repr__(self):
        return 'PlottingConfiguration for a 1D OT algoritm'

    #_________________________

    def plotter(self):
        return Plotter(self)

    #_________________________

    def defaultAttributes(self):
        DefaultConfiguration.defaultAttributes(self)

        self.addAttribute('EPSILON',
                          defaultVal=1.e-8,
                          isSubAttr=[],
                          attrType='float')

        self.addAttribute('singleOrMulti',
                          defaultVal='multi')

        self.addAttribute('figDir',
                          defaultVal='./figures/')

        self.addAttribute('extensions',
                          defaultVal=['.pdf'],
                          attrType='list')

        self.addAttribute('outputDirList',
                          defaultVal=['./output/'],
                          attrType='list')

        self.addAttribute('labelList',
                          defaultVal=['sim0'],
                          attrType='list')

        #_______________

        self.addAttribute('plotAnalyse',
                          defaultVal=True,
                          attrType='bool')

        self.addAttribute('plotAnalyse_plotSubplotsFunction',
                          defaultVal='customPlotSubplots',
                          isSubAttr=[('plotAnalyse', True)])

        self.addAttribute('plotAnalyse_prefixFigName',
                          defaultVal='analyse_',
                          isSubAttr=[('plotAnalyse', True)])

        self.addAttribute('plotAnalyse_plotSubplots_iterOrTime',
                          defaultVal='iterations',
                          isSubAttr=[('plotAnalyse', True)])

        self.addAttribute('plotAnalyse_plotSubplots_xScale',
                          defaultVal='log',
                          isSubAttr=[('plotAnalyse', True)])

        self.addAttribute('plotAnalyse_plotSubplots_yScale',
                          defaultVal='log',
                          isSubAttr=[('plotAnalyse', True)])

        self.addAttribute('plotAnalyse_plotSubplots_grid',
                          defaultVal=True,
                          isSubAttr=[('plotAnalyse', True)],
                          attrType='bool')

        #_______________

        self.addAttribute('plotFinalState',
                          True, 
                          [],
                          'bool',
                          True)

        self.addAttribute('plotFinalState_prefixFigName',
                          'finalState_', 
                          [('plotFinalState', True)],
                          'str',
                          True)

        self.addAttribute('plotFinalState_transparencyFunction',
                          'customTransparency', 
                          [('plotFinalState', True)],
                          'str',
                          True)

        self.addAttribute('plotFinalState_legend',
                          True, 
                          [('plotFinalState', True)],
                          'bool',
                          True)

        self.addAttribute('plotFinalState_grid',
                          True,
                          [('plotFinalState', True)],
                          'bool',
                          True)

        self.addAttribute('plotFinalState_timeTextPBar',
                          True,
                          [('plotFinalState', True)],
                          'bool',
                          True)

        self.addAttribute('plotFinalState_xLabel',
                          '', 
                          [('plotFinalState', True)],
                          'str',
                          False)

        self.addAttribute('plotFinalState_yLabel',
                          '', 
                          [('plotFinalState', True)],
                          'str',
                          False)

        self.addAttribute('plotFinalState_extendX',
                          0.0, 
                          [('plotFinalState', True)],
                          'float',
                          True)

        self.addAttribute('plotFinalState_extendY',
                          0.0, 
                          [('plotFinalState', True)],
                          'float',
                          True)

        self.addAttribute('plotFinalState_nbrXTicks',
                          2, 
                          [('plotFinalState', True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_nbrYTicks',
                          2, 
                          [('plotFinalState', True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_xTicksDecimals',
                          2, 
                          [('plotFinalState', True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_yTicksDecimals',
                          2, 
                          [('plotFinalState', True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_order',
                          'horizontalFirst', 
                          [('plotFinalState', True)],
                          'str',
                          True)

        self.addAttribute('plotFinalState_extendDirection',
                          'vertical', 
                          [('plotFinalState', True)],
                          'str',
                          True)

#__________________________________________________
