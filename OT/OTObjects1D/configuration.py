#____________________
# Class Configuration
#____________________
#
# Defines everything necessary for running an OT algorithm from a config file
#

from .boundaries.defineBoundaries                import boundariesForConfig
from .algorithms.adr.adrAlgorithm                import AdrAlgorithm
from .algorithms.pd.pdAlgorithm                  import PdAlgorithm
from .algorithms.adr3.adr3Algorithm              import Adr3Algorithm
from .algorithms.anamorph.anamorphAlgorithm      import AnamorphAlgorithm
from .algorithms.project.projectAlgorithm        import ProjectAlgorithm
from ..utils.configuration.defaultConfiguration import DefaultConfiguration

#__________________________________________________

class Configuration(DefaultConfiguration):
    '''
    Stores the configuraion for an OT algorithm
    '''

    def __init__(self, configFile=None):
        DefaultConfiguration.__init__(self, configFile)
        self.swappedInitFinal = False
        self.iterCount = 0
        boundariesForConfig(self)

    #_________________________

    def __repr__(self):
        return 'Configuration for a 1D OT algoritm'

    #_________________________

    def algorithm(self):
        if self.algoName == 'adr':
            return AdrAlgorithm(self)
        elif self.algoName == 'pd':
            return PdAlgorithm(self)
        elif self.algoName == 'adr3':
            return Adr3Algorithm(self)
        elif self.algoName == 'anamorph':
            return AnamorphAlgorithm(self)
        elif self.algoName == 'project':
            return ProjectAlgorithm(self)
        else:
            return

    #_________________________

    def checkAttributes(self):
        DefaultConfiguration.checkAttributes(self)
        
        if self.algoName == 'adr':
            if not self.gamma > self.EPSILON:
                print ( 'Value ' + self.gamma +
                        ' is not valid for parameter gamma ' )
                self.gamma = self.defaultValues['gamma']
                print ( 'Replacing by default value : ' + str ( self.gamma ) )
            if not ( self.alpha > self.EPSILON and self.alpha < 2. - self.EPSILON ):
                print ( 'Value ' + self.alpha +
                        ' is not valid for parameter alpha ' )
                self.alpha = self.defaultValues['alpha']
                print ( 'Replacing by default value : ' + str ( self.alpha ) )
                
        elif self.algoName == 'pd':
            if not ( self.theta >= 0. and self.theta <= 1. ):
                print ( 'Value ' + self.theta +
                        ' is not valid for parameter theta ' )
                self.theta = self.defaultValues['theta']
                print ( 'Replacing by default value : ' + str ( self.theta ) )
            if not ( self.sigma * self.tau < 1. - self.EPSILON ):
                print ( 'Values ' + str(self.sigma) + ' and ' + str(self.tau) +
                        'are not valid for parameters sigma and tau ')
                self.sigma = self.defaultValues['sigma']
                self.tau   = self.defaultValues['tau']
                print ( 'Replacing by default values : ' + str(self.sigma) + ' and ' +str(self.tau) ) 

        elif self.algoName == 'adr3':
            if not self.gamma3 > self.EPSILON:
                print ( 'Value ' + self.gamma3 +
                        ' is not valid for parameter gamma3 ' )
                self.gamma3 = self.defaultValues['gamma3']
                print ( 'Replacing by default value : ' + str ( self.gamma3 ) )
            if not ( self.alpha3 > self.EPSILON and self.alpha3 < 2. - self.EPSILON ):
                print ( 'Value ' + self.alpha3 +
                        ' is not valid for parameter alpha3 ' )
                self.alpha3 = self.defaultValues['alpha3']
                print ( 'Replacing by default value : ' + str ( self.alpha3 ) )

            if not ( self.omega1 > self.EPSILON and self.omega1 <= 1. ):
                print ( 'Value ' + self.omega1 +
                        ' is not valid for parameter omega1 ' )
                self.omega1 = self.defaultValues['omega1']
                print ( 'Replacing by default value : ' + str ( self.omega1 ) )

            if not ( self.omega2 > self.EPSILON and self.omega2 <= 1. ):
                print ( 'Value ' + self.omega2 +
                        ' is not valid for parameter omega2 ' )
                self.omega2 = self.defaultValues['omega2']
                print ( 'Replacing by default value : ' + str ( self.omega2 ) )

            if not ( self.omega3 > self.EPSILON and self.omega3 <= 1. ):
                print ( 'Value ' + self.omega3 +
                        ' is not valid for parameter omega3 ' )
                self.omega3 = self.defaultValues['omega3']
                print ( 'Replacing by default value : ' + str ( self.omega3 ) )

            if ( not ( self.omega1 + self.omega2 + self.omega3 > 1. - self.EPSILON ) or
                 not ( self.omega1 + self.omega2 + self.omega3 < 1. + self.EPSILON ) ):
                print ( 'Values ' + str(self.omega1) + ', ' + str(self.omega2) + ' and ' + str(self.omega3) +
                        'are not valid for parameters omega1, omega2 and omega3 ')
                self.omega1 = self.defaultValues['omega1']
                self.omega2 = self.defaultValues['omega2']
                self.omega3 = self.defaultValues['omega3']
                print ( 'Replacing by default values : ' + str(self.omega1) + ', ' + str(self.omega2) + ' and ' +str(self.omega3) )

    #_________________________

    def defaultAttributes(self):
        DefaultConfiguration.defaultAttributes(self)

        self.addAttribute('EPSILON',
                          defaultVal=1.e-8,
                          attrType='float')

        self.addAttribute('outputDir',
                          defaultVal='./output/')

        self.addAttribute('N',
                          defaultVal=32,
                          attrType='int')

        self.addAttribute('P',
                          defaultVal=32,
                          attrType='int')

        self.addAttribute('fineResolution',
                          defaultVal=1000,
                          attrType='int')

        self.addAttribute('dynamics',
                          defaultVal=0,
                          attrType='int')

        self.addAttribute('boundaryType',
                          defaultVal=1,
                          attrType='int')

        self.addAttribute('normType',
                          defaultVal=0,
                          attrType='int')

        self.addAttribute('filef0',
                          defaultVal='f0.bin',
                          isSubAttr=[('boundaryType',0)])

        self.addAttribute('filef1',
                          defaultVal='f1.bin',
                          isSubAttr=[('boundaryType',0)])

        self.addAttribute('filem0',
                          defaultVal='m0.bin',
                          isSubAttr=[('boundaryType',0),('dynamics',0)])

        self.addAttribute('filem1',
                          defaultVal='m1.bin',
                          isSubAttr=[('boundaryType',0),('dynamics',0)])

        self.addAttribute('algoName',
                          defaultVal='adr')

        self.addAttribute('iterTarget',
                          defaultVal=1000,
                          attrType='int')

        self.addAttribute('nModPrint',
                          defaultVal=100,
                          attrType='int')

        self.addAttribute('nModWrite',
                          defaultVal=100,
                          attrType='int')

        self.addAttribute('initial',
                          defaultVal=0,
                          attrType='int')

        self.addAttribute('initialInputDir',
                          defaultVal='./',
                          printWarning=False)

        self.addAttribute('gamma',
                          defaultVal=1./75.,
                          isSubAttr=[('algoName','adr')],
                          attrType='float')

        self.addAttribute('alpha',
                          defaultVal=1.998,
                          isSubAttr=[('algoName','adr')],
                          attrType='float')

        self.addAttribute('tau',
                          defaultVal=0.99/85.,
                          isSubAttr=[('algoName','pd')],
                          attrType='float')

        self.addAttribute('sigma',
                          defaultVal=85.,
                          isSubAttr=[('algoName','pd')],
                          attrType='float')

        self.addAttribute('theta',
                          defaultVal=1.0,
                          isSubAttr=[('algoName','pd')],
                          attrType='float')

        self.addAttribute('gamma3',
                          defaultVal=1./75.,
                          isSubAttr=[('algoName','adr3')],
                          attrType='float')

        self.addAttribute('alpha3',
                          defaultVal=1.998,
                          isSubAttr=[('algoName','adr3')],
                          attrType='float')

        self.addAttribute('omega1',
                          defaultVal=0.33,
                          isSubAttr=[('algoName','adr3')],
                          attrType='float')

        self.addAttribute('omega2',
                          defaultVal=0.33,
                          isSubAttr=[('algoName','adr3')],
                          attrType='float')

        self.addAttribute('omega3',
                          defaultVal=0.33,
                          isSubAttr=[('algoName','adr3')],
                          attrType='float')

        self.addAttribute('PDFError',
                          defaultVal=0.001,
                          isSubAttr=[('algoName','anamorph')],
                          attrType='float')

#__________________________________________________
