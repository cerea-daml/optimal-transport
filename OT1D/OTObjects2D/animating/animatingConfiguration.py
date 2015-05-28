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
        return 'AnimatingConfiguration for a 2D OT algoritm'

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
                          './figures/',
                          [],
                          False,
                          False,
                          str)

        self.addAttribute('writerName',
                          'ffmpeg',
                          [],
                          False,
                          False,
                          str)

        self.addAttribute('writerFPS',
                          5,
                          [],
                          False,
                          False,
                          int)

        self.addAttribute('writerCodec',
                          None,
                          [],
                          False,
                          False,
                          str)

        self.addAttribute('writerBitrate',
                          None,
                          [],
                          False,
                          False,
                          int)

        self.addAttribute('writerExtraArgs',
                          None,
                          [],
                          True,
                          False,
                          str)

        self.addAttribute('extension',
                          ['.mp4'],
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
        
        self.addAttribute('funcAnimArgs',
                          None,
                          [],
                          False,
                          True,
                          None)

        self.addAttribute('animFinalState',
                          1,
                          [],
                          False,
                          False,
                          int)

        self.addAttribute('animFinalState_prefixFigName',
                          'finalState',
                          [('animFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('animFinalState_transparencyFunction',
                          'customTransparency',
                          [('animFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('animFinalState_Plotter',
                          'imshow',
                          [('animFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('animFinalState_Args',
                          None,
                          [('animFinalState',1)],
                          False,
                          True,
                          None)

        self.addAttribute('animFinalState_ArgsInit',
                          None,
                          [('animFinalState',1)],
                          False,
                          True,
                          None)

        self.addAttribute('animFinalState_ArgsFinal',
                          None,
                          [('animFinalState',1)],
                          False,
                          True,
                          None)

        self.addAttribute('animFinalState_colorBar',
                          1,
                          [('animFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('animFinalState_cmapName',
                          'jet',
                          [('animFinalState_colorBar',1)],
                          False,
                          False,
                          str)

        self.addAttribute('animFinalState_timeTextPBar',
                          1,
                          [('animFinalState',1)],
                          False,
                          False,
                          int)


        self.addAttribute('animFinalState_xLabel',
                          '',
                          [('animFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('animFinalState_yLabel',
                          '',
                          [('animFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('animFinalState_cLabel',
                          '',
                          [('animFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('animFinalState_extendX',
                          0.0,
                          [('animFinalState',1)],
                          False,
                          False,
                          float)

        self.addAttribute('animFinalState_extendY',
                          0.0,
                          [('animFinalState',1)],
                          False,
                          False,
                          float)

        self.addAttribute('animFinalState_nbrXTicks',
                          0,
                          [('animFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('animFinalState_nbrYTicks',
                          0,
                          [('animFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('animFinalState_nbrCTicks',
                          0,
                          [('animFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('animFinalState_xTicksRound',
                          1,
                          [('animFinalState',1)],
                          False,
                          False,
                          int)


        self.addAttribute('animFinalState_yTicksRound',
                          1,
                          [('animFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('animFinalState_cTicksRound',
                          1,
                          [('animFinalState',1)],
                          False,
                          False,
                          int)

        self.addAttribute('animFinalState_order',
                          'horizontalFirst',
                          [('animFinalState',1)],
                          False,
                          False,
                          str)

        self.addAttribute('animFinalState_extendDirection',
                          'vertical',
                          [('animFinalState',1)],
                          False,
                          False,
                          str)
