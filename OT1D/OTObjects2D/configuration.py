#####################
# Class Configuration
#####################
#
# Defines everything necessary for running an OT algorithm from a config file
#

from boundaries.defineBoundaries import boundariesForConfig
from algorithms.adr.adrAlgorithm import AdrAlgorithm
from algorithms.pd.pdAlgorithm import PdAlgorithm
from algorithms.adr3.adr3Algorithm import Adr3Algorithm

class Configuration(object):
    '''
    Stores the configuraion for an OT algorithm
    '''

    def __init__(self, configFile=None):
        self.defaultAttributes()
        self.fromfile(configFile)
        self.ckeckAttributes()
        self.iterCount = 0
        boundariesForConfig(self)

    def __repr__(self):
        return 'Configuration for a 1D OT algoritm'

    def algorithm(self):
        if self.algoName == 'adr':
            return AdrAlgorithm(self)
        elif self.algoName == 'pd':
            return PdAlgorithm(self)
        elif self.algoName == 'adr3':
            return Adr3Algorithm(self)
        else:
            return

    def printConfig(self):
        nbrChar = 0
        for attr in self.attributes:
            nbrChar = max( nbrChar , len( attr ) )
        nbrChar += 1

        attributes = []
        for attr in self.attributes:
            while len(attr) < nbrChar:
                attr += ' '
            attributes.append(attr + ': ')

        for (attrToPrint,attr,subattr) in zip(attributes,self.attributes,self.isSubAttribute):
            if subattr is None:
                print ( attrToPrint + str( self.__getattribute__(attr) ) )
            else:
                (parentattr,parentval) = subattr
                if self.__getattribute__( parentattr ) == parentval:
                    print ( attrToPrint + str( self.__getattribute__(attr) ) )

    def ckeckAttributes(self):
        for (attr,val,subattr,type) in zip(self.attributes,self.defaultValues,self.isSubAttribute,self.attributeType):
            if subattr is None:
                if self.__dict__.has_key(attr):
                    try:
                        self.__setattr__( attr , type( self.__getattribute__( attr ) ) )
                    except:
                        print ( 'Value ' + str( self.__getattribute__( attr ) ) + 
                                ' is not valid for parameter ' + str ( attr ) )
                        print ( 'Replacing by default value : ' + str ( val ) )
                        self.__setattr__( attr , val )
                else:
                    print ( 'No Value found for parameter ' + str( attr ) )
                    print ( 'Replacing by default value : ' + str ( val ) )
                    self.__setattr__( attr , val )

        for (attr,val,subattr,type) in zip(self.attributes,self.defaultValues,self.isSubAttribute,self.attributeType):
            if not subattr is None:
                (parentattr,parentval) = subattr
                if self.__getattribute__( parentattr ) == parentval:
                    if self.__dict__.has_key(attr):
                        try:
                            self.__setattr__( attr , type( self.__getattribute__( attr ) ) )
                        except:
                            print ( 'Value ' + str( self.__getattribute__( attr ) ) +
                                    ' is not valid for parameter ' + str ( attr ) )
                            print ( 'Replacing by default value : ' + str ( val ) )
                            self.__setattr__( attr , val )
                    else:
                        print ( 'No Value found for parameter ' + str( attr ) )
                        print ( 'Replacing by default value : ' + str ( val ) )
                        self.__setattr__( attr , val )

        if self.algoName == 'adr':
            if not self.gamma > self.EPSILON:
                print ( 'Value ' + self.gamma +
                        ' is not valid for parameter gamma ' )
                self.gamma = defaultValueFor(self,'gamma')
                print ( 'Replacing by default value : ' + str ( self.gamma ) )
            if not ( self.alpha > self.EPSILON and self.alpha < 2. - self.EPSILON ):
                print ( 'Value ' + self.alpha +
                        ' is not valid for parameter alpha ' )
                self.alpha = defaultValueFor(self,'alpha')
                print ( 'Replacing by default value : ' + str ( self.alpha ) )
                
        elif self.algoName == 'pd':
            if not ( self.theta >= 0. and self.theta <= 1. ):
                print ( 'Value ' + self.theta +
                        ' is not valid for parameter theta ' )
                self.theta = defaultValueFor(self,'theta')
                print ( 'Replacing by default value : ' + str ( self.theta ) )
            if not ( self.sigma * self.tau < 1. - self.EPSILON ):
                print ( 'Values ' + str(self.sigma) + ' and ' + str(self.tau) +
                        'are not valid for parameters sigma and tau ')
                self.sigma = defaultValueFor(self,'sigma')
                self.tau = defaultValueFor(self,'tau')
                print ( 'Replacing by default values : ' + str(self.sigma) + ' and ' +str(self.tau) ) 

        elif self.algoName == 'adr3':
            if not self.gamma3 > self.EPSILON:
                print ( 'Value ' + self.gamma3 +
                        ' is not valid for parameter gamma3 ' )
                self.gamma3 = defaultValueFor(self,'gamma3')
                print ( 'Replacing by default value : ' + str ( self.gamma3 ) )
            if not ( self.alpha3 > self.EPSILON and self.alpha3 < 2. - self.EPSILON ):
                print ( 'Value ' + self.alpha3 +
                        ' is not valid for parameter alpha3 ' )
                self.alpha3 = defaultValueFor(self,'alpha3')
                print ( 'Replacing by default value : ' + str ( self.alpha3 ) )

            if not ( self.omega1 > self.EPSILON and self.omega1 <= 1. ):
                print ( 'Value ' + self.omega1 +
                        ' is not valid for parameter omega1 ' )
                self.omega1 = defaultValueFor(self,'omega1')
                print ( 'Replacing by default value : ' + str ( self.omega1 ) )

            if not ( self.omega2 > self.EPSILON and self.omega2 <= 1. ):
                print ( 'Value ' + self.omega2 +
                        ' is not valid for parameter omega2 ' )
                self.omega2 = defaultValueFor(self,'omega2')
                print ( 'Replacing by default value : ' + str ( self.omega2 ) )

            if not ( self.omega3 > self.EPSILON and self.omega3 <= 1. ):
                print ( 'Value ' + self.omega3 +
                        ' is not valid for parameter omega3 ' )
                self.omega3 = defaultValueFor(self,'omega3')
                print ( 'Replacing by default value : ' + str ( self.omega3 ) )

            if ( not ( self.omega1 + self.omega2 + self.omega3 > 1. - self.EPSILON ) or
                 not ( self.omega1 + self.omega2 + self.omega3 < 1. + self.EPSILON ) ):
                print ( 'Values ' + str(self.omega1) + ', ' + str(self.omega2) + ' and ' + str(self.omega3) +
                        'are not valid for parameters omega1, omega2 and omega3 ')
                self.omega1 = defaultValueFor(self,'omega1')
                self.omega2 = defaultValueFor(self,'omega2')
                self.omega3 = defaultValueFor(self,'omega3')
                print ( 'Replacing by default values : ' + str(self.omega1) + ', ' + str(self.omega2) + ' and ' +str(self.omega3) )

    def fromfile(self, fileName):
        if ('config.bin' in fileName):
            try:
                f = open(fileName,'rb')
                p = Unpickler(f)
                try:
                    while True:
                        config = p.load()
                except:
                    self = config
                    f.close()
                    return
            except:
                return

        try:
            f = open(fileName,'r')
            lines = f.readlines()
            f.close()
        except:
            return

        filteredLines = []
        for line in lines:
            l = line.strip().replace(' ','').split('#')[0]
            if not l == '':
                filteredLines.append(l)

        for line in filteredLines:
            try:
                l = line.split('=')
                attrName = l[0]
                attrValue = l[1]

                for (attribute,type) in zip(self.attributes,self.attributeType):
                    if attrName == attribute:
                        self.__setattr__(attrName,type(attrValue))
            except:
                pass

    def defaultAttributes(self):
        self.attributes = []
        self.defaultValues = []
        self.isSubAttribute = []
        self.attributeType = []

        self.attributes.append('EPSILON')
        self.defaultValues.append(1.e-8)
        self.isSubAttribute.append(None)
        self.attributeType.append(float)

        self.attributes.append('outputDir')
        self.defaultValues.append('./output/')
        self.isSubAttribute.append(None)
        self.attributeType.append(str)

        self.attributes.append('M')
        self.defaultValues.append(32)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('N')
        self.defaultValues.append(32)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('P')
        self.defaultValues.append(32)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('dynamics')
        self.defaultValues.append(0)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('boundaryType')
        self.defaultValues.append(1)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('normType')
        self.defaultValues.append(0)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('filef0')
        self.defaultValues.append('f0.bin')
        self.isSubAttribute.append(('boundaryType',0))
        self.attributeType.append(str)

        self.attributes.append('filef1')
        self.defaultValues.append('f1.bin')
        self.isSubAttribute.append(('boundaryType',0))
        self.attributeType.append(str)

        self.attributes.append('filemx0')
        self.defaultValues.append('mx0.bin')
        self.isSubAttribute.append(('boundaryType',0))
        self.attributeType.append(str)

        self.attributes.append('filemx1')
        self.defaultValues.append('mx1.bin')
        self.isSubAttribute.append(('boundaryType',0))
        self.attributeType.append(str)

        self.attributes.append('filemy0')
        self.defaultValues.append('my0.bin')
        self.isSubAttribute.append(('boundaryType',0))
        self.attributeType.append(str)

        self.attributes.append('filemy1')
        self.defaultValues.append('my1.bin')
        self.isSubAttribute.append(('boundaryType',0))
        self.attributeType.append(str)

        self.attributes.append('algoName')
        self.defaultValues.append('adr')
        self.isSubAttribute.append(None)
        self.attributeType.append(str)

        self.attributes.append('iterTarget')
        self.defaultValues.append(10000)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('nModPrint')
        self.defaultValues.append(500)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('nModWrite')
        self.defaultValues.append(500)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('initial')
        self.defaultValues.append(0)
        self.isSubAttribute.append(None)
        self.attributeType.append(int)

        self.attributes.append('initialInputDir')
        self.defaultValues.append('./')
        self.isSubAttribute.append(('initial',1))
        self.attributeType.append(str)

        self.attributes.append('gamma')
        self.defaultValues.append(1./75.)
        self.isSubAttribute.append(('algoName','adr'))
        self.attributeType.append(float)

        self.attributes.append('alpha')
        self.defaultValues.append(1.998)
        self.isSubAttribute.append(('algoName','adr'))
        self.attributeType.append(float)

        self.attributes.append('tau')
        self.defaultValues.append(0.99/85.)
        self.isSubAttribute.append(('algoName','pd'))
        self.attributeType.append(float)

        self.attributes.append('sigma')
        self.defaultValues.append(85.)
        self.isSubAttribute.append(('algoName','pd'))
        self.attributeType.append(float)

        self.attributes.append('theta')
        self.defaultValues.append(1.0)
        self.isSubAttribute.append(('algoName','pd'))
        self.attributeType.append(float)

        self.attributes.append('gamma3')
        self.defaultValues.append(1./75.)
        self.isSubAttribute.append(('algoName','adr3'))
        self.attributeType.append(float)

        self.attributes.append('alpha3')
        self.defaultValues.append(1.998)
        self.isSubAttribute.append(('algoName','adr3'))
        self.attributeType.append(float)

        self.attributes.append('omega1')
        self.defaultValues.append(0.33)
        self.isSubAttribute.append(('algoName','adr3'))
        self.attributeType.append(float)

        self.attributes.append('omega2')
        self.defaultValues.append(0.33)
        self.isSubAttribute.append(('algoName','adr3'))
        self.attributeType.append(float)

        self.attributes.append('omega3')
        self.defaultValues.append(0.34)
        self.isSubAttribute.append(('algoName','adr3'))
        self.attributeType.append(float)

    def defaultValueFor(self,attrName):
        for (attr,val) in zip(self.attributes,self.defaultValues):
            if attr == attrName:
                return val
        return None
