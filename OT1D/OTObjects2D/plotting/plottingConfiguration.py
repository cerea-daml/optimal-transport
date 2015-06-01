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

    def __init__(self, plottingConfigFile=None):
        DefaultConfiguration.__init__(self, plottingConfigFile)

    def __repr__(self):
        return 'PlottingConfiguration for a 2D OT algoritm'

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
                          'float',
                          True)

        self.addAttribute('singleOrMulti',
                          0,
                          [],
                          'int',
                          True)

        self.addAttribute('figDir',
                          './figures/',
                          [],
                          'str',
                          True)

        self.addAttribute('extension',
                          ['.pdf'],
                          [],
                          'list',
                          True)

        self.addAttribute('outputDir',
                          ['./output/'],
                          [],
                          'list',
                          True)

        self.addAttribute('label',
                          ['sim0'],
                          [],
                          'list',
                          True)

        self.addAttribute('plotAnalyse',
                          True,
                          [],
                          'bool',
                          True)

        self.addAttribute('plotAnalyse_plotSubplotsFunction',
                          'customPlotSubplots',
                          [('plotAnalyse', True)],
                          'str',
                          True)

        self.addAttribute('plotAnalyse_prefixFigName',
                          'analyse_',
                          [('plotAnalyse', True)],
                          'str',
                          True)

        self.addAttribute('plotAnalyse_plotSubplots_iterOrTime',
                          'iterations',
                          [('plotAnalyse', True)],
                          'str',
                          True)

        self.addAttribute('plotAnalyse_plotSubplots_xScale',
                          'log',
                          [('plotAnalyse', True)],
                          'str',
                          True)

        self.addAttribute('plotAnalyse_plotSubplots_yScale',
                          'log',
                          [('plotAnalyse', True)],
                          'str',
                          True)

        self.addAttribute('plotAnalyse_plotSubplots_grid',
                          True,
                          [('plotAnalyse', True)],
                          'bool',
                          True)

        self.addAttribute('plotFinalState',
                          True,
                          [],
                          'bool',
                          True)

        self.addAttribute('plotFinalState_prefixFigName',
                          'finalState_',
                          [('plotFinalState',True)],
                          'str',
                          True)

        self.addAttribute('plotFinalState_transparencyFunction',
                          'customTransparency',
                          [('plotFinalState',True)],
                          'str',
                          True)

        self.addAttribute('plotFinalState_plotter',
                          'imshow',
                          [('plotFinalState',True)],
                          'str',
                          True)

        self.addAttribute('plotFinalState_args',
                          {},
                          [('plotFinalState',True)],
                          'dict',
                          True)

        self.addAttribute('plotFinalState_argsInit',
                          {},
                          [('plotFinalState',True)],
                          'dict',
                          True)

        self.addAttribute('plotFinalState_argsFinal',
                          {},
                          [('plotFinalState',True)],
                          'dict',
                          True)

        self.addAttribute('plotFinalState_colorBar',
                          True,
                          [('plotFinalState',True)],
                          'bool',
                          True)

        self.addAttribute('plotFinalState_cmapName',
                          'jet',
                          [('plotFinalState_colorBar',True)],
                          'str',
                          True)

        self.addAttribute('plotFinalState_timeTextPBar',
                          True,
                          [('plotFinalState',True)],
                          'bool',
                          True)

        self.addAttribute('plotFinalState_xLabel',
                          '',
                          [('plotFinalState',True)],
                          'str',
                          False)

        self.addAttribute('plotFinalState_yLabel',
                          '',
                          [('plotFinalState',True)],
                          'str',
                          False)

        self.addAttribute('plotFinalState_cLabel',
                          '',
                          [('plotFinalState',True)],
                          'str',
                          False)

        self.addAttribute('plotFinalState_extendX',
                          0.0,
                          [('plotFinalState',True)],
                          'float',
                          True)

        self.addAttribute('plotFinalState_extendY',
                          0.0,
                          [('plotFinalState',True)],
                          'float',
                          True)

        self.addAttribute('plotFinalState_nbrXTicks',
                          2,
                          [('plotFinalState',True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_nbrYTicks',
                          2,
                          [('plotFinalState',True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_nbrCTicks',
                          5,
                          [('plotFinalState',True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_xTicksDecimals',
                          1,
                          [('plotFinalState',True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_yTicksDecimals',
                          1,
                          [('plotFinalState',True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_cTicksDecimals',
                          2,
                          [('plotFinalState',True)],
                          'int',
                          True)

        self.addAttribute('plotFinalState_order',
                          'horizontalFirst',
                          [('plotFinalState',True)],
                          'str',
                          True)

        self.addAttribute('plotFinalState_extendDirection',
                          'horizontal',
                          [('plotFinalState',True)],
                          'str',
                          True)
