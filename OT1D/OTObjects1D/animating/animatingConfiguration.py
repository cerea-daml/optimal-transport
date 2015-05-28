##############################
# Class AnimatingConfiguration
##############################
#
# Defines everything necessary for animating the result of an OT algorithm from a config file
#

from animator import Animator

from ...utils.io.io                              import fileNameSuffix
from ...utils.configuration.defaultConfiguration import DefaultConfiguration

class AnimatingConfiguration(DefaultConfiguration):

    def __init__(self, animatingConfigFile=None):
        DefaultConfiguration.__init__(self, animatingConfigFile)

    def __repr__(self):
        return 'AnimatingConfiguration for a 1D OT algoritm'

    def animator(self):
        return Animator(self)

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

        self.addAttribute('writerName',
                          'ffmpeg',
                          [],
                          'str',
                          True)

        self.addAttribute('writerFPS',
                          5,
                          [],
                          'int',
                          False)

        self.addAttribute('writerCodec',
                          None,
                          [],
                          'str',
                          False)

        self.addAttribute('writerBitrate',
                          None,
                          [],
                          'int',
                          False)

        self.addAttribute('writerExtraArgs',
                          None,
                          [],
                          'list',
                          False)

        self.addAttribute('extension',
                          ['.mp4'],
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

        self.addAttribute('funcAnimArgs',
                          {},
                          [],
                          'dict',
                          False)

        self.addAttribute('animFinalState',
                          True,
                          [],
                          'bool',
                          True)

        self.addAttribute('animFinalState_prefixFigName',
                          'finalState_',
                          [('animFinalState', True)],
                          'str',
                          True)

        self.addAttribute('animFinalState_transparencyFunction',
                          'customTransparency',
                          [('animFinalState', True)],
                          'str',
                          True)

        self.addAttribute('animFinalState_legend',
                          True,
                          [('animFinalState', True)],
                          'bool',
                          True)

        self.addAttribute('animFinalState_grid',
                          True,
                          [('animFinalState', True)],
                          'bool',
                          True)

        self.addAttribute('animFinalState_timeTextPBar',
                          True,
                          [('animFinalState', True)],
                          'bool',
                          True)

        self.addAttribute('animFinalState_xLabel',
                          '',
                          [('animFinalState', True)],
                          'str',
                          False)

        self.addAttribute('animFinalState_yLabel',
                          '',
                          [('animFinalState', True)],
                          'str',
                          False)

        self.addAttribute('animFinalState_extendX',
                          0.0,
                          [('animFinalState', True)],
                          'float',
                          True)

        self.addAttribute('animFinalState_extendY',
                          0.0,
                          [('animFinalState', True)],
                          'float',
                          True)

        self.addAttribute('animFinalState_nbrXTicks',
                          2,
                          [('animFinalState', True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_nbrYTicks',
                          2,
                          [('animFinalState', True)],
                          'int',
                          True)
        self.addAttribute('animFinalState_xTicksDecimals',
                          2,
                          [('animFinalState', True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_yTicksDecimals',
                          2,
                          [('animFinalState', True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_order',
                          'horizontalFirst',
                          [('animFinalState', True)],
                          'str',
                          True)

        self.addAttribute('animFinalState_extendDirection',
                          'vertical',
                          [('animFinalState', True)],
                          'str',
                          True)

