#####################
# Class Configuration
#####################
#
# Defines everything necessary for running an OT algorithm from a config file
#

from boundaries.defineBoundaries import boundariesForConfig
from algorithms.adr.adrAlgorithm import AdrAlgorithm
from algorithms.pd.pdAlgorithm import PdAlgorithm

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

        self.attributes.append('filem0')
        self.defaultValues.append('m0.bin')
        self.isSubAttribute.append(('boundaryType',0))
        self.attributeType.append(str)

        self.attributes.append('filem1')
        self.defaultValues.append('m1.bin')
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

    def defaultValueFor(self,attrName):
        for (attr,val) in zip(self.attributes,self.defaultValues):
            if attr == attrName:
                return val
        return None
