#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#_____________________________
# Class AnimatingConfiguration
#_____________________________
#
# Defines everything necessary for animating the result of an OT algorithm from a config file
#

from animator                                    import Animator
from ...utils.io.io                              import fileNameSuffix
from ...utils.configuration.defaultConfiguration import DefaultConfiguration

#__________________________________________________

class AnimatingConfiguration(DefaultConfiguration):

    def __init__(self, animatingConfigFile=None):
        DefaultConfiguration.__init__(self, animatingConfigFile)

        i    = len(self.labelList)
        iMax = len(self.outputDirList)

        while i < iMax:
            self.labelList.append('sim'+fileNameSuffix(i, iMax))
            i += 1

    #_________________________

    def __repr__(self):
        return 'AnimatingConfiguration for a 1D OT algoritm'

    #_________________________

    def animator(self):
        return Animator(self)

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
                          defaultVal=['.mp4'],
                          attrType='list')

        self.addAttribute('outputDirList',
                          defaultVal=['./output/'],
                          attrType='list')

        self.addAttribute('labelList',
                          defaultVal=['sim0'],
                          attrType='list')

        #_______________

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

        self.addAttribute('funcAnimArgs',
                          {},
                          [],
                          'dict',
                          False)

        #_______________

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

#__________________________________________________
