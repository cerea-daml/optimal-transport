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
        return 'AnimatingConfiguration for a 2D OT algoritm'

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

        self.addAttribute('animFinalState_plotter',
                          'imshow',
                          [('animFinalState',True)],
                          'str',
                          True)

        self.addAttribute('animFinalState_args',
                          {},
                          [('animFinalState',True)],
                          'dict',
                          True)

        self.addAttribute('animFinalState_argsInit',
                          {},
                          [('animFinalState',True)],
                          'dict',
                          True)

        self.addAttribute('animFinalState_argsFinal',
                          {},
                          [('animFinalState',True)],
                          'dict',
                          True)

        self.addAttribute('animFinalState_colorBar',
                          True,
                          [('animFinalState',True)],
                          'bool',
                          True)

        self.addAttribute('animFinalState_cmapName',
                          'jet',
                          [('animFinalState',True)],
                          'str',
                          True)

        self.addAttribute('animFinalState_timeTextPBar',
                          True,
                          [('animFinalState',True)],
                          'str',
                          True)

        self.addAttribute('animFinalState_xLabel',
                          '',
                          [('animFinalState',True)],
                          'str',
                          False)

        self.addAttribute('animFinalState_yLabel',
                          '',
                          [('animFinalState',True)],
                          'str',
                          False)

        self.addAttribute('animFinalState_cLabel',
                          '',
                          [('animFinalState',True)],
                          'str',
                          False)

        self.addAttribute('animFinalState_extendX',
                          0.0,
                          [('animFinalState',True)],
                          'float',
                          True)

        self.addAttribute('animFinalState_extendY',
                          0.0,
                          [('animFinalState',True)],
                          'float',
                          True)

        self.addAttribute('animFinalState_nbrXTicks',
                          2,
                          [('animFinalState',True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_nbrYTicks',
                          2,
                          [('animFinalState',True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_nbrCTicks',
                          5,
                          [('animFinalState',True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_xTicksDecimals',
                          1,
                          [('animFinalState',True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_yTicksDecimals',
                          1,
                          [('animFinalState',True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_cTicksDecimals',
                          2,
                          [('animFinalState',True)],
                          'int',
                          True)

        self.addAttribute('animFinalState_order',
                          'horizontalFirst',
                          [('animFinalState',True)],
                          'str',
                          True)

        self.addAttribute('animFinalState_extendDirection',
                          'vertical',
                          [('animFinalState',True)],
                          'str',
                          True)

        #_______________

        self.addAttribute('trianimFinalState',
                          defaultVal=True,
                          attrType='bool')

        self.addAttribute('trianimFinalState_prefixFigName',
                          defaultVal='finalState_tri_',
                          isSubAttr=[('trianimFinalState',True)])

        self.addAttribute('trianimFinalState_plotter',
                          defaultVal='imshow',
                          isSubAttr=[('trianimFinalState',True)])

        self.addAttribute('trianimFinalState_args',
                          defaultVal={},
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='dict')

        self.addAttribute('trianimFinalState_colorBar',
                          defaultVal=True,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='bool')

        self.addAttribute('trianimFinalState_cmapName',
                          defaultVal='jet',
                          isSubAttr=[('trianimFinalState',True)])

        self.addAttribute('trianimFinalState_timeTextPBar',
                          defaultVal=True,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='bool')

        self.addAttribute('trianimFinalState_xLabel',
                          defaultVal='',
                          isSubAttr=[('trianimFinalState',True)])

        self.addAttribute('trianimFinalState_yLabel',
                          defaultVal='',
                          isSubAttr=[('trianimFinalState',True)])

        self.addAttribute('trianimFinalState_cLabel',
                          defaultVal='',
                          isSubAttr=[('trianimFinalState',True)])

        self.addAttribute('trianimFinalState_extendX',
                          defaultVal=0.0,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='float')

        self.addAttribute('trianimFinalState_extendY',
                          defaultVal=0.0,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='float')

        self.addAttribute('trianimFinalState_nbrXTicks',
                          defaultVal=2,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='int')

        self.addAttribute('trianimFinalState_nbrYTicks',
                          defaultVal=2,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='int')

        self.addAttribute('trianimFinalState_nbrCTicks',
                          defaultVal=5,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='int')

        self.addAttribute('trianimFinalState_xTicksDecimals',
                          defaultVal=1,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='int')

        self.addAttribute('trianimFinalState_yTicksDecimals',
                          defaultVal=1,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='int')

        self.addAttribute('trianimFinalState_cTicksDecimals',
                          defaultVal=2,
                          isSubAttr=[('trianimFinalState',True)],
                          attrType='int')

        self.addAttribute('trianimFinalState_order',
                          defaultVal='horizontalFirst',
                          isSubAttr=[('trianimFinalState',True)])

        self.addAttribute('trianimFinalState_extendDirection',
                          defaultVal='vertical',
                          isSubAttr=[('trianimFinalState',True)])

        self.addAttribute('trianimFinalState_extendDirectionTrianim',
                          defaultVal='horizontal',
                          isSubAttr=[('trianimFinalState',True)])

#__________________________________________________
