#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#####################
# defineBoundaries.py
#####################
#
# Function boundariesForConfig returns boundary conditions for the given configuration
#

import numpy as np
from scipy.interpolate import interp1d

from ...utils.io.io import extensionOfFile
from ...utils.io.io import arrayFromFile
from ..grid         import grid

from gaussian       import defaultBoundaryGaussian
from gaussian       import defaultBoundaryGaussian2
from gaussianSplit  import defaultBoundaryGaussianSplit1
from gaussianSplit  import defaultBoundaryGaussianSplit2
from gaussianSine   import defaultBoundaryGaussianSine
from gaussianSine   import defaultBoundaryGaussianCosine
from custom         import customBoundary
from custom         import customBoundaryRev

def boundariesForConfig(config):
    # default configurations
    if config.boundaryType == 1:
        config.boundaries = defaultBoundaryGaussian( config.N , config.P )
    elif config.boundaryType == 2:
        config.boundaries = defaultBoundaryGaussian2( config.N , config.P )
    elif config.boundaryType == 3:
        config.boundaries = defaultBoundaryGaussianSplit1( config.N , config.P )
    elif config.boundaryType == 4:
        config.boundaries = defaultBoundaryGaussianSplit2( config.N , config.P )
    elif config.boundaryType == 5:
        config.boundaries = defaultBoundaryGaussianSine( config.N , config.P )
    elif config.boundaryType == 6:
        config.boundaries = defaultBoundaryGaussianCosine( config.N , config.P )
    elif config.boundaryType == 7:
        config.boundaries = customBoundary( config.N, config.P )
    elif config.boundaryType == 8:
        config.boundaries = customBoundaryRev( config.N, config.P )

    # from file
    elif config.boundaryType == 0:
        config.boundaries = boundariesFromFile( config )

    # normalize boundaries
    config.boundaries.normalize(config.normType)

    # adapt boundaries to dynamics
    if config.dynamics == 1:
        config.boundaries.spatialBoundaries = grid.SpatialBoundaries( config.N , config.P )

    if config.dynamics == 0 or config.dynamics == 1:
        delta = config.boundaries.relativeMassDefault()
        if delta > config.EPSILON:
            print ('Changing dynamics because mass default is not compatible with dynamics=0.')

            if config.algoName == 'pd':
                config.dynamics = 2
            else:
                N = config.N
                bt0 = np.zeros(N+1+2)
                bt1 = np.zeros(N+1+2)
                bt0[1:N+2] = config.boundaries.temporalBoundaries.bt0[:]
                bt1[1:N+2] = config.boundaries.temporalBoundaries.bt1[:]
                temporalBoundaries = TemporalBoundaries( N+2, config.P, bt0, bt1 )

                config.boundaries = Boundaries( N+2 , config.P , temporalBoundaries )
                config.N = N+2
                
                if config.algoName == 'adr':
                    config.dynamics = 3
                elif config.algoName == 'adr3':
                    config.dynamics = 4

    if config.dynamics == 2:
        config.boundaries.spatialBoundaries = grid.SpatialBoundaries( config.N , config.P )
    elif config.dynamics == 3 or config.dynamics == 4:
        config.boundaries.spatialBoundaries = grid.SpatialBoundaries( config.N , config.P )
        config.boundaries.placeReservoir(config)

def boundariesFromFile(config):
    bt0 = arrayFromFile( config.filef0 )
    bt1 = arrayFromFile( config.filef1 )

    if bt0 is None or bt1 is None:
        raise IOError('Could not load temporal boundaries')

    try:
        bt0 = np.array(bt0)
        bt1 = np.array(bt1)
    except:
        raise IOError('Could not cast temporal boundaries into arrays')

    if ( not len(bt0.shape) == 1 or
         not len(bt1.shape) == 1 ):
        raise IOError('Temporal boundaries must be 1-dimensional arrays')

    if not bt0.size == config.N + 1:
        print( 'Interpolating bt0 into OT resolution ...')
        bt0temp = bt0.copy()
        interpBt0 = interp1d( np.linspace( 0.0 , 1.0 , bt0.size ) , bt0temp )
        bt0 = interpBt0( np.linspace( 0.0 , 1.0 , config.N + 1 ) )

    if not bt1.size == config.N + 1:
        print( 'Interpolating bt1 into OT resolution ...')
        bt1temp = bt1.copy()
        interpBt1 = interp1d( np.linspace( 0.0 , 1.0 , bt1.size ) , bt1temp )
        bt1 = interpBt1( np.linspace( 0.0 , 1.0 , config.N + 1 ) )

    temporalBoundaries = grid.TemporalBoundaries( config.N , config.P , bt0 , bt1 )

    if not config.dynamics == 0:
        spatialBoundaries = grid.SpatialBoundaries( config.N , config.P )
        return grid.Boundaries( config.N , config.P , temporalBoundaries , spatialBoundaries )

    bx0 = arrayFromFile( config.filem0 )
    bx1 = arrayFromFile( config.filem1 )

    if bx0 is None or bx1 is None:
        raise IOError('Could not load spatial boundaries')

    try:
        bx0 = np.array(bx0)
        bx1 = np.array(bx1)
    except:
        raise IOError('Could not cast spatial boundaries into arrays')

    if ( not len(bx0.shape) == 1 or
         not len(bx1.shape) == 1 ):
        raise IOError('Spatial boundaries must be 1-dimensional arrays')

    if not bx0.size == config.P + 1:
        print( 'Interpolating bx0 into OT resolution ...')
        bx0temp = bx0.copy()
        interpBx0 = interp1d( np.linspace( 0.0 , 1.0 , bx0.size ) , bx0temp )
        bx0 = interpBx0( np.linspace( 0.0 , 1.0 , config.P + 1 ) )

    if not bx1.size == config.P + 1:
        print( 'Interpolating bx1 into OT resolution ...')
        bx1temp = bx1.copy()
        interpBx1 = interp1d( np.linspace( 0.0 , 1.0 , bx1.size ) , bx1temp )
        bx1 = interpBx1( np.linspace( 0.0 , 1.0 , config.P + 1 ) )

    spatialBoundaries = grid.SpatialBoundaries( config.N , config.P , bx0 , bx1 )
    
    return grid.Boundaries( config.N , config.P , temporalBoundaries , spatialBoundaries )
