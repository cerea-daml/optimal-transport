#############################
# Class AnimatingConfiguration
#############################
#
# Defines everything necessary for animating the result of an OT algorithm from a config file
#

from animator import Animator

from ...utils.io.io                              import fileNameSuffix
from ...utils.configuration.defaultConfiguration import DefaultConfiguration

class AnimatorConfiguration(DefaultConfiguration):
    '''
    Stores the configuraion for animating a 1D OT algorithm
    '''

    def __init__(self, plottingConfigFile=None):
        DefaultConfiguration.__init__(self, plottingConfigFile)

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
        self.attributeType['writerCodec']               = int

        self.attributes.append('writerBitrate')
        self.defaultValues['writerBitrate']             = None
        self.isSubAttribute['writerBitrate']            = []
        self.isList['writerBitrate']                    = False
        self.isDict['writerBitrate']                    = False
        self.attributeType['writerBitrate']             = {}

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

        self.attributes.append('prefixFigNameFinalState')
        self.defaultValues['prefixFigNameFinalState']   = 'finalState'
        self.isSubAttribute['prefixFigNameFinalState']  = []
        self.isList['prefixFigNameFinalState']          = False
        self.isDict['prefixFigNameFinalState']          = False
        self.attributeType['prefixFigNameFinalState']   = str

        self.attributes.append('transparencyFunctionName')
        self.defaultValues['transparencyFunctionName']  = 'customTransparency'
        self.isSubAttribute['transparencyFunctionName'] = []
        self.isList['transparencyFunctionName']         = False
        self.isDict['transparencyFunctionName']         = False
        self.attributeType['transparencyFunctionName']  = str
