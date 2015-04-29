#####################
# Class Configuration
#####################
#
# Defines everything necessary for running an OT algorithm from a config file
#

import pickle as pck

from boundaries.defineBoundaries import boundariesForConfig

from adr.adrAlgorithm import AdrAlgorithm

class Configuration:
    '''
    Stores the configuraion for an OT algorithm
    '''

    def __init__(self, configFile=None):

        self.fromfile(configFile)
        self.default()
        self.iterCount = 0
        boundariesForConfig(self)

    def algorithm(self):
        if self.algoName == 'adr':
            return AdrAlgorithm(config)

        else:
            return

    def printConfig(self):
        print('EPSILON :'+str(self.EPSILON))
        print('outputDir :'+self.outputDir)
        print('N :'+str(self.N))
        print('P :'+str(self.P))
        print('dynamics :'+str(self.dynamics))
        print('boundaryType :'+str(self.boundaryType))
        print('normType :'+str(self.normType))

        if self.boundaryType == 0:
            print('file for f0 :'+str(self.filef0))
            print('file for f1 :'+str(self.filef1))

            if self.dynamics == 0:
                print('file for m0 :'+str(self.filem0))
                print('file for m1 :'+str(self.filem1))

        print('algoName :'+str(self.algoName))
        print('iterTarge :'+str(self.iterTarget))
        print('nModPrint :'+str(self.nModPrint))
        print('nModWrite :'+str(self.nModWrite))

        if self.algoName == 'adr':
            print('gamma :'+str(self.gamma))
            print('alpha :'+str(self.alpha))

        else:
            pass

    def default(self):
        try:
            self.EPSILON
        except:
            self.EPSILON = 1.e-8
            print('No value for EPSILON')
            print('Default value :'+self.EPSILON)

        try:
            self.outputDir
        except:
            self.outputDir = './outputOT/'
            print('No value for outputDir')
            print('Default value :'+self.outputDir)

        try:
            self.N
        except:
            self.N = 32
            print('No value for N')
            print('Default value :'+str(self.N))

        try:
            self.P
        except:
            self.P = 32
            print('No value for P')
            print('Default value :'+str(self.P))

        try:
            self.dynamics
        except:
            self.dynamics = 0
            print('No value for dynamics')
            print('Default value :'+str(self.dynamics))
            
        try:
            self.boundaryType
        except:
            self.boundaryType = 1
            print('No value for boundaryType')
            print('Default value :'+str(self.boundaryType))

        try:
            self.normType
        except:
            self.normType = 0
            print('No value for normType')
            print('Default value :'+str(self.normType))

        if self.boundaryType == 0:
            try:
                self.filef0
            except:
                self.filef0 = 'f0.npy'
                print('No value for filef0')
                print('Default value :'+str(self.filef0))
            try:
                self.filef1
            except:
                self.filef1 = 'f1.npy'
                print('No value for filef1')
                print('Default value :'+str(self.filef1))

            if self.dynamics == 0:
                try:
                    self.filem0
                except:
                    self.filem0 = 'm0.npy'
                    print('No value for filem0')
                    print('Default value :'+str(self.filem0))

                try:
                    self.filem1
                except:
                    self.filem1 = 'm1.npy'
                    print('No value for filem1')
                    print('Default value :'+str(self.filem1))

        try:
            self.algoName
        except:
            self.algoName = 'adr'
            print('No value for algoName')
            print('Default value :'+str(self.algoName))

        try:
            self.iterTarget
        except:
            self.iterTarget = 10000
            print('No value for iterTarget')
            print('Default value :'+str(self.iterTarget))

        try:
            self.nModPrint
        except:
            self.nModPrint = 500
            print('No value for nModPrint')
            print('Default value :'+str(self.nModPrint))

        try:
            self.nModWrite
        except:
            self.nModWrite = 500
            print('No value for nModWrite')
            print('Default value :'+str(self.nModWrite))

        if self.algoName == 'adr':
            try:
                self.gamma
            except:
                self.gamma = 1./75.
                print('No value for gamma')
                print('Default value :'+str(self.gamma))
            try:
                self.alpha
            except:
                self.alpha = 1.998
                print('No value for alpha')
                print('Default value :'+str(self.alpha))

        else:
            self.gamma = 1./75.

    def fromfile(self, fileName):
        if ('config.bin' in fileName):
            try:
                f = open(fileName,'rb')
                p = Unpickler(f)
                while True:
                    config = p.load()
            self = config
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
            if ('outputDir:' in line):
                try:
                    self.outputDir = line.split(':')[1]
            elif ('EPSILON:' in line):
                try:
                    self.EPSILON = float(line.split(':')[1])
            elif ('N:' in line):
                try:
                    self.N = int(line.split(':')[1])
            elif ('P:' in line):
                try:
                    self.P = int(line.split(':')[1])
            elif ('dynamics:' in line):
                try:
                    self.dynamics = int(line.split(':')[1])
            elif ('boundaryType:' in line):
                try:
                    self.boundaryType = int(line.split(':')[1])
            elif ('normType:' in line):
                try:
                    self.normType = int(line.split(':')[1])
            elif ('filef0:' in line):
                try:
                    self.filef0 = line.split(':')[1]
            elif ('filef1:' in line):
                try:
                    self.filef1 = line.split(':')[1]
            elif ('filem0:' in line):
                try:
                    self.filem0 = line.split(':')[1]
            elif ('filem1:' in line):
                try:
                    self.filem1 = line.split(':')[1]
            elif ('algoName:' in line):
                try:
                    self.algoName = line.split(':')[1]
            elif ('iterTarget:' in line):
                try:
                    self.iterTarget = int(line.split(':')[1])
            elif ('nModPrint:' in line):
                try:
                    self.nModPrint = int(line.split(':')[1])
            elif ('nModWrite:' in line):
                try:
                    self.nModWrite = int(line.split(':')[1])
            elif ('gamma:' in line):
                try:
                    self.gamma = float(line.split(':')[1])
            elif ('alpha:' in line):
                try:
                    self.alpha = float(line.split(':')[1])
