#############################
# Class PlottingConfiguration
#############################
#
# Defines everything necessary for plotting the result of an OT algorithm from a config file
#

from plotter import Plotter

from ...utils.configuration.defaultConfiguration import DefaultConfiguration
from ...utils.io.io                              import fileNameSuffix

class PlottingConfiguration(DefaultConfiguration):
    '''
    Stores the configuraion for plotting a 2d OT algorithm
    '''

    def __init__(self, plottingConfigFile=None):
        DefaultConfiguration.__init__(self, plottingConfigFile)

    def __repr__(self):
        return 'PlottingConfiguration for a 2d OT algoritm'

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

        self.addAttribute('EPSILON',
                          1.e-8,
                          [],
                          False,
                          False,
                          float)

        self.addAttribute('singleOrMulti',
                          0,
                          [],
                          False,
                          False,
                          int)

        self.addAttribute('figDir',
                          ['./figures/'],
                          [],
                          False,
                          False,
                          str)

        self.addAttribute('extension',
                          ['.pdf'],
                          [],
                          True,
                          False,
                          str)
        
        self.addAttribute('outputDir',
                          ['./output/'],
                          [],
                          True,
                          False,
                          str)

        self.addAttribute('label',
                          ['sim0'],
                          [],
                          True,
                          False,
                          str)

        self.addAttribute('plotAnalyse',
                          1,
                          [],
                          False,
                          False,
                          int)

        self.addAttribute('plotSubplotsFunctionName',
                          'customPlotSubplots',
                          [('plotAnalyse', 1)],
                          False,
                          False,
                          str)

        self.addAttribute('prefixFigNameAnalyse',
                          'analyse',
                          [('plotAnalyse', 1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotSubplotsFunctionArgs',
                          None,
                          [('plotAnalyse', 1)],
                          False,
                          True,
                          None)

        self.addAttribute('plotFinalState',
                          1,
                          [],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_prefixFigName',
                          'finalState',
                          [('plotFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotFinalState_transparencyFunction',
                          'customTransparency',
                          [('plotFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotFinalState_Plotter',
                          'imshow',
                          [('plotFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotFinalState_Args',
                          None,
                          [('plotFinalState',1)],
                          False,
                          True,
                          None)

        self.addAttribute('plotFinalState_ArgsInit',
                          None,
                          [('plotFinalState',1)],
                          False,
                          True,
                          None)

        self.addAttribute('plotFinalState_ArgsFinal',
                          None,
                          [('plotFinalState',1)],
                          False,
                          True,
                          None)

        self.addAttribute('plotFinalState_colorBar',
                          1,
                          [('plotFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_cmapName',
                          'jet',
                          [('plotFinalState_colorBar',1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotFinalState_timeTextPBar',
                          1,
                          [('plotFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_xLabel',
                          '',
                          [('plotFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotFinalState_yLabel',
                          '',
                          [('plotFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotFinalState_cLabel',
                          '',
                          [('plotFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotFinalState_extendX',
                          0.0,
                          [('plotFinalState',1)],
                          False,
                          False,
                          float)

        self.addAttribute('plotFinalState_extendY',
                          0.0,
                          [('plotFinalState',1)],
                          False,
                          False,
                          float)

        self.addAttribute('plotFinalState_nbrXTicks',
                          0,
                          [('plotFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_nbrYTicks',
                          0,
                          [('plotFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_nbrCTicks',
                          0,
                          [('plotFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_xTicksRound',
                          1,
                          [('plotFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_yTicksRound',
                          1,
                          [('plotFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_cTicksRound',
                          1,
                          [('plotFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('plotFinalState_order',
                          'horizontalFirst',
                          [('plotFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('plotFinalState_extendDirection',
                          'vertical',
                          [('plotFinalState',1)],
                          False,
                          False,
                          str)
