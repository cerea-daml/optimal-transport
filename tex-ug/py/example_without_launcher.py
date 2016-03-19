#!/usr/bin/env python

import numpy as np
from OT.OTObjects1D.algorithms.pd.pdAlgorithm import PdAlgorithm
from OT.OTObjects1D.grid                      import grid

# Main parameters
outputDir  = '/wherever/you/want/'
N          = 31
P          = 31
sigma      = 85.0
tau        = 1.0 / 85.0
theta      = 1.0
iterTarget = 10000
nModPrint  = 1000
nModWrite  = 1000

# Empty class configuration
class Configuration:
    # You just need this function for the run of the algorithm
    def printConfig(self):
        print('Print the message you want')

# Boundary conditions
# f0 ( x )  = A0 exp ( - alphaX0 * ( x - x0 ) ^ 2 )
# f1 ( x )  = A1 exp ( - alphaX1 * ( x - x1 ) ^ 2 )
A0      = 1.0
alphaX0 = 60.0
x0      = 0.375
A1      = 1.0
alphaX1 = 60.0
x1      = 0.625
X       = np.linspace ( 0.0 , 1.0 , N + 1 )
f0      = A0 * np.exp ( - alphaX0 * np.power ( X - x0 ,  2.0 )  )
f1      = A1 * np.exp ( - alphaX1 * np.power ( X - x1 ,  2.0 )  )

tBounds = grid.TemporalBoundaries( N , P , f0 , f1 )
sBounds = grid.SpatialBoundaries( N , P )
bounds  = grid.Boundaries( N , P , tlBounds, sBounds )

# Fill configuration with the parameters
config            = Configuration() ;
config.N          = N
config.P          = P
config.iterTarget = iterTarget
config.nModPrint  = nModPrint
config.nModWrite  = nModWrite
config.dynamics   = 0
config.boundaries = bounds
config.outputDir  = outputDir
config.initial    = 0
config.sigma      = sigma
config.tau        = tau
config.theta      = theta

# Constructs the algorithm and run it
algo = PdAlgorithm(config)
algo.run()
