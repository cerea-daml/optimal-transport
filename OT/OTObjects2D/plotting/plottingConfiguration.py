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

from .plotter                                     import Plotter
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
        return 'PlottingConfiguration for a 2D OT algoritm'

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
                          defaultVal=True,
                          attrType='bool')

        self.addAttribute('plotFinalState_prefixFigName',
                          defaultVal='finalState_',
                          isSubAttr=[('plotFinalState',True)])

        self.addAttribute('plotFinalState_transparencyFunction',
                          defaultVal='customTransparency',
                          isSubAttr=[('plotFinalState',True)])

        self.addAttribute('plotFinalState_plotter',
                          defaultVal='imshow',
                          isSubAttr=[('plotFinalState',True)])

        self.addAttribute('plotFinalState_args',
                          defaultVal={},
                          isSubAttr=[('plotFinalState',True)],
                          attrType='dict')

        self.addAttribute('plotFinalState_argsInit',
                          defaultVal={},
                          isSubAttr=[('plotFinalState',True)],
                          attrType='dict')

        self.addAttribute('plotFinalState_argsFinal',
                          defaultVal={},
                          isSubAttr=[('plotFinalState',True)],
                          attrType='dict')

        self.addAttribute('plotFinalState_colorBar',
                          defaultVal=True,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='bool')

        self.addAttribute('plotFinalState_cmapName',
                          defaultVal='jet',
                          isSubAttr=[('plotFinalState',True)])

        self.addAttribute('plotFinalState_timeTextPBar',
                          defaultVal=True,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='bool')

        self.addAttribute('plotFinalState_xLabel',
                          defaultVal='',
                          isSubAttr=[('plotFinalState',True)])

        self.addAttribute('plotFinalState_yLabel',
                          defaultVal='',
                          isSubAttr=[('plotFinalState',True)])

        self.addAttribute('plotFinalState_cLabel',
                          defaultVal='',
                          isSubAttr=[('plotFinalState',True)])

        self.addAttribute('plotFinalState_extendX',
                          defaultVal=0.0,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='float')

        self.addAttribute('plotFinalState_extendY',
                          defaultVal=0.0,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='float')

        self.addAttribute('plotFinalState_nbrXTicks',
                          defaultVal=2,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='int')

        self.addAttribute('plotFinalState_nbrYTicks',
                          defaultVal=2,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='int')

        self.addAttribute('plotFinalState_nbrCTicks',
                          defaultVal=5,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='int')

        self.addAttribute('plotFinalState_xTicksDecimals',
                          defaultVal=1,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='int')

        self.addAttribute('plotFinalState_yTicksDecimals',
                          defaultVal=1,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='int')

        self.addAttribute('plotFinalState_cTicksDecimals',
                          defaultVal=2,
                          isSubAttr=[('plotFinalState',True)],
                          attrType='int')

        self.addAttribute('plotFinalState_order',
                          defaultVal='horizontalFirst',
                          isSubAttr=[('plotFinalState',True)])

        self.addAttribute('plotFinalState_extendDirection',
                          defaultVal='horizontal',
                          isSubAttr=[('plotFinalState',True)])

        #_______________

        self.addAttribute('triplotFinalState',
                          defaultVal=True,
                          attrType='bool')

        self.addAttribute('triplotFinalState_prefixFigName',
                          defaultVal='finalState_tri_',
                          isSubAttr=[('triplotFinalState',True)])

        self.addAttribute('triplotFinalState_plotter',
                          defaultVal='imshow',
                          isSubAttr=[('triplotFinalState',True)])

        self.addAttribute('triplotFinalState_args',
                          defaultVal={},
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='dict')

        self.addAttribute('triplotFinalState_colorBar',
                          defaultVal=True,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='bool')

        self.addAttribute('triplotFinalState_cmapName',
                          defaultVal='jet',
                          isSubAttr=[('triplotFinalState',True)])

        self.addAttribute('triplotFinalState_timeTextPBar',
                          defaultVal=True,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='bool')

        self.addAttribute('triplotFinalState_xLabel',
                          defaultVal='',
                          isSubAttr=[('triplotFinalState',True)])

        self.addAttribute('triplotFinalState_yLabel',
                          defaultVal='',
                          isSubAttr=[('triplotFinalState',True)])

        self.addAttribute('triplotFinalState_cLabel',
                          defaultVal='',
                          isSubAttr=[('triplotFinalState',True)])

        self.addAttribute('triplotFinalState_extendX',
                          defaultVal=0.0,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='float')

        self.addAttribute('triplotFinalState_extendY',
                          defaultVal=0.0,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='float')

        self.addAttribute('triplotFinalState_nbrXTicks',
                          defaultVal=2,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='int')

        self.addAttribute('triplotFinalState_nbrYTicks',
                          defaultVal=2,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='int')

        self.addAttribute('triplotFinalState_nbrCTicks',
                          defaultVal=5,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='int')

        self.addAttribute('triplotFinalState_xTicksDecimals',
                          defaultVal=1,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='int')

        self.addAttribute('triplotFinalState_yTicksDecimals',
                          defaultVal=1,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='int')

        self.addAttribute('triplotFinalState_cTicksDecimals',
                          defaultVal=2,
                          isSubAttr=[('triplotFinalState',True)],
                          attrType='int')

        self.addAttribute('triplotFinalState_order',
                          defaultVal='horizontalFirst',
                          isSubAttr=[('triplotFinalState',True)])

        self.addAttribute('triplotFinalState_extendDirection',
                          defaultVal='vertical',
                          isSubAttr=[('triplotFinalState',True)])

        self.addAttribute('triplotFinalState_extendDirectionTriplot',
                          defaultVal='horizontal',
                          isSubAttr=[('triplotFinalState',True)])

#__________________________________________________
