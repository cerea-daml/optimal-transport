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

        self.attributes.append('writerName')
        self.defaultValues['writerName']                = 'ffmpeg'
        self.isSubAttribute['writerName']               = []
        self.isList['writerName']                       = False
        self.isDict['writerName']                       = False
        self.attributeType['writerName']                = str

        self.attributes.append('writerFPS')
        self.defaultValues['writerFPS']                 = 5
        self.isSubAttribute['writerFPS']                = []
        self.isList['writerFPS']                        = False
        self.isDict['writerFPS']                        = False
        self.attributeType['writerFPS']                 = int

        self.attributes.append('writerCodec')
        self.defaultValues['writerCodec']               = None
        self.isSubAttribute['writerCodec']              = []
        self.isList['writerCodec']                      = False
        self.isDict['writerCodec']                      = False
        self.attributeType['writerCodec']               = str

        self.attributes.append('writerBitrate')
        self.defaultValues['writerBitrate']             = None
        self.isSubAttribute['writerBitrate']            = []
        self.isList['writerBitrate']                    = False
        self.isDict['writerBitrate']                    = False
        self.attributeType['writerBitrate']             = int

        self.attributes.append('writerExtraArgs')
        self.defaultValues['writerExtraArgs']           = None
        self.isSubAttribute['writerExtraArgs']          = []
        self.isList['writerExtraArgs']                  = True
        self.isDict['writerExtraArgs']                  = False
        self.attributeType['writerExtraArgs']           = str

        self.attributes.append('extension')
        self.defaultValues['extension']                 = ['.pdf']
        self.isSubAttribute['extension']                = []
        self.isList['extension']                        = True
        self.isDict['extension']                        = False
        self.attributeType['extension']                 = str

        self.attributes.append('funcAnimArgs')
        self.defaultValues['funcAnimArgs']              = None
        self.isSubAttribute['funcAnimArgs']             = []
        self.isList['funcAnimArgs']                     = False
        self.isDict['funcAnimArgs']                     = True
        self.attributeType['funcAnimArgs']              = None

        self.attributes.append('outputDir')
        self.defaultValues['outputDir']                 = ['./output/']
        self.isSubAttribute['outputDir']                = []
        self.isList['outputDir']                        = True
        self.isDict['outputDir']                        = False
        self.attributeType['outputDir']                 = str

        self.attributes.append('label')
        self.defaultValues['label']                     = ['']
        self.isSubAttribute['label']                    = []
        self.isList['label']                            = True
        self.isDict['label']                            = False
        self.attributeType['label']                     = str

        self.attributes.append('animFinalState')
        self.defaultValues['animFinalState']            = 1 
        self.isSubAttribute['animFinalState']           = []
        self.isList['animFinalState']                   = False
        self.isDict['animFinalState']                   = False
        self.attributeType['animFinalState']            = int

        self.attributes.append('animFinalState_prefixFigName')
        self.defaultValues['animFinalState_prefixFigName']         = 'finalState'
        self.isSubAttribute['animFinalState_prefixFigName']        = [('animFinalState',1)]
        self.isList['animFinalState_prefixFigName']                = False
        self.isDict['animFinalState_prefixFigName']                = False
        self.attributeType['animFinalState_prefixFigName']         = str

        self.attributes.append('animFinalState_transparencyFunction')
        self.defaultValues['animFinalState_transparencyFunction']  = 'customTransparency'
        self.isSubAttribute['animFinalState_transparencyFunction'] = [('animFinalState',1)]
        self.isList['animFinalState_transparencyFunction']         = False
        self.isDict['animFinalState_transparencyFunction']         = False
        self.attributeType['animFinalState_transparencyFunction']  = str

        self.attributes.append('animFinalState_addLegend')
        self.defaultValues['animFinalState_addLegend']             = 1
        self.isSubAttribute['animFinalState_addLegend']            = [('animFinalState',1)]
        self.isList['animFinalState_addLegend']                    = False
        self.isDict['animFinalState_addLegend']                    = False
        self.attributeType['animFinalState_addLegend']             = int

        self.attributes.append('animFinalState_grid')
        self.defaultValues['animFinalState_grid']                  = 1
        self.isSubAttribute['animFinalState_grid']                 = [('animFinalState',1)]
        self.isList['animFinalState_grid']                         = False
        self.isDict['animFinalState_grid']                         = False
        self.attributeType['animFinalState_grid']                  = int

        self.attributes.append('animFinalState_addTimeTextPbar')
        self.defaultValues['animFinalState_addTimeTextPbar']       = 1
        self.isSubAttribute['animFinalState_addTimeTextPbar']      = [('animFinalState',1)]
        self.isList['animFinalState_addTimeTextPbar']              = False
        self.isDict['animFinalState_addTimeTextPbar']              = False
        self.attributeType['animFinalState_addTimeTextPbar']       = int

        self.attributes.append('animFinalState_xLabel')
        self.defaultValues['animFinalState_xLabel']                = ''
        self.isSubAttribute['animFinalState_xLabel']               = [('animFinalState',1)]
        self.isList['animFinalState_xLabel']                       = False
        self.isDict['animFinalState_xLabel']                       = False
        self.attributeType['animFinalState_xLabel']                = str

        self.attributes.append('animFinalState_yLabel')
        self.defaultValues['animFinalState_yLabel']                = None
        self.isSubAttribute['animFinalState_yLabel']               = [('animFinalState',1)]
        self.isList['animFinalState_yLabel']                       = False
        self.isDict['animFinalState_yLabel']                       = False
        self.attributeType['animFinalState_yLabel']                = str

        self.attributes.append('animFinalState_nbrXTicks')
        self.defaultValues['animFinalState_nbrXTicks']             = 3
        self.isSubAttribute['animFinalState_nbrXTicks']            = [('animFinalState',1)]
        self.isList['animFinalState_nbrXTicks']                    = False
        self.isDict['animFinalState_nbrXTicks']                    = False
        self.attributeType['animFinalState_nbrXTicks']             = int

        self.attributes.append('animFinalState_nbrYTicks')
        self.defaultValues['animFinalState_nbrYTicks']             = 3
        self.isSubAttribute['animFinalState_nbrYTicks']            = [('animFinalState',1)]
        self.isList['animFinalState_nbrYTicks']                    = False
        self.isDict['animFinalState_nbrYTicks']                    = False
        self.attributeType['animFinalState_nbrYTicks']             = int

        self.attributes.append('animFinalState_xTicksRound')
        self.defaultValues['animFinalState_xTicksRound']           = 1
        self.isSubAttribute['animFinalState_xTicksRound']          = [('animFinalState',1)]
        self.isList['animFinalState_xTicksRound']                  = False
        self.isDict['animFinalState_xTicksRound']                  = False
        self.attributeType['animFinalState_xTicksRound']           = int

        self.attributes.append('animFinalState_yTicksRound')
        self.defaultValues['animFinalState_yTicksRound']           = 1
        self.isSubAttribute['animFinalState_yTicksRound']          = [('animFinalState',1)]
        self.isList['animFinalState_yTicksRound']                  = False
        self.isDict['animFinalState_yTicksRound']                  = False
        self.attributeType['animFinalState_yTicksRound']           = int

        self.attributes.append('animFinalState_order')
        self.defaultValues['animFinalState_order']                 = 'horizontalFirst'
        self.isSubAttribute['animFinalState_order']                = [('animFinalState',1)]
        self.isList['animFinalState_order']                        = False
        self.isDict['animFinalState_order']                        = False
        self.attributeType['animFinalState_order']                 = str

        self.attributes.append('animFinalState_extendDirection')
        self.defaultValues['animFinalState_extendDirection']       = 'vertical'
        self.isSubAttribute['animFinalState_extendDirection']      = [('animFinalState',1)]
        self.isList['animFinalState_extendDirection']              = False
        self.isDict['animFinalState_extendDirection']              = False
        self.attributeType['animFinalState_extendDirection']       = str

