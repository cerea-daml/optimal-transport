#####################
# defineBoundaries.py
#####################
#
# Function boundariesForConfig returns boundary conditions for the given configuration
#

import numpy as np
from .scipy.interpolate import interp1d

from ...utils.io.io import extensionOfFile
from ...utils.io.io import arrayFromFile
from ..grid         import grid

from .gaussian       import defaultBoundaryGaussian
from .gaussian       import defaultBoundaryGaussian2
from .gaussianSplit  import defaultBoundaryGaussianSplit1
from .gaussianSplit  import defaultBoundaryGaussianSplit2
from .gaussianSine   import defaultBoundaryGaussianSine
from .gaussianSine   import defaultBoundaryGaussianCosine

def boundariesForConfig(config):
    # default configurations
    if config.boundaryType == 1:
        config.boundaries = defaultBoundaryGaussian( config.M , config.N , config.P )
    elif config.boundaryType == 2:
        config.boundaries = defaultBoundaryGaussian2( config.M , config.N , config.P )
    elif config.boundaryType == 3:
        config.boundaries = defaultBoundaryGaussianSplit1( config.M , config.N , config.P )
    elif config.boundaryType == 4:
        config.boundaries = defaultBoundaryGaussianSplit2( config.M , config.N , config.P )
    elif config.boundaryType == 5:
        config.boundaries = defaultBoundaryGaussianSine( config.M , config.N , config.P )
    elif config.boundaryType == 6:
        config.boundaries = defaultBoundaryGaussianCosine( config.M , config.N , config.P )

    # from file
    elif config.boundaryType == 0:
        config.boundaries = boundariesFromFile( config )

    # normalize boundaries
    config.boundaries.normalize(config.normType)
    
    # adapt boundaries to dynamics
    if config.dynamics == 1:
        config.boundaries.spatialBoundaries = grid.SpatialBoundaries( config.M , config.N , config.P )

    if config.dynamics == 0 or config.dynamics == 1:
        delta = config.boundaries.relativeMassDefault()
        if delta > config.EPSILON:
            print ('Changing dynamics because mass default is not compatible with dynamics='+str(config.dynamics))

            if config.algoName == 'pd':
                config.dynamics = 2
            else:
                M = config.M
                N = config.N
                bt0 = np.zeros(shape=(M+1+2,N+1+2))
                bt1 = np.zeros(shape=(M+1+2,N+1+2))
                bt0[1:M+2,1:N+2] = config.boundaries.temporalBoundaries.bt0[:,:]
                bt1[1:M+2,1:N+2] = config.boundaries.temporalBoundaries.bt1[:,:]
                temporalBoundaries = TemporalBoundaries( M+2, N+2, config.P, bt0, bt1 )

                config.boundaries = Boundaries( M+2, N+2 , config.P , temporalBoundaries )
                config.M = M+2
                config.N = N+2
                
                if config.algoName == 'adr':
                    config.dynamics = 3
                elif config.algoName == 'adr3':
                    config.dynamics = 4

    if config.dynamics == 2:
        config.boundaries.spatialBoundaries = grid.SpatialBoundaries( config.M , config.N , config.P )
    elif config.dynamics == 3 or config.dynamics == 4:
        config.boundaries.spatialBoundaries = grid.SpatialBoundaries( config.M , config.N , config.P )
        config.boundaries.placeReservoir(config)

def boundariesFromFile(config):
    # Catching bt from files
    bt0 = arrayFromFile( config.filef0 )
    bt1 = arrayFromFile( config.filef1 )

    if bt0 is None or bt1 is None:
        raise IOError('Could not load temporal boundaries')

    try:
        bt0 = np.array(bt0)
        bt1 = np.array(bt1)
    except:
        raise IOError('Could not cast temporal boundaries into arrays')

    if len(bt0.shape) == 1:
        bt0 = bt0.reshape((config.M+1,config.N+1))

    if len(bt1.shape) == 1:
        bt1 = bt1.reshape((config.M+1,config.N+1))

    if ( not len(bt0.shape) == 2 or
         not len(bt1.shape) == 2 ):
        raise IOError('Temporal boundaries must be 2-dimensional arrays')

    if not bt0.shape == (config.M+1,config.N+1):
        print( 'Interpolating bt0 into OT resolution ...')

        if not bt0.shape[0] == config.M + 1:
            bt0temp = bt0.copy()
            interpBt0 = interp1d( np.linspace( 0.0 , 1.0 , bt0.shape[0] ) , bt0temp , axis = 0 )
            bt0 = interpBt0( np.linspace( 0.0 , 1.0 , config.M + 1 ) )

        if not bt0.shape[1] == config.N + 1:
            bt0temp = bt0.copy()
            interpBt0 = interp1d( np.linspace( 0.0 , 1.0 , bt0.shape[1] ) , bt0temp , axis = 1 )
            bt0 = interpBt0( np.linspace( 0.0 , 1.0 , config.N + 1 ) )

    if not bt1.shape == (config.M+1,config.N+1):
        print( 'Interpolating bt1 into OT resolution ...')

        if not bt1.shape[0] == config.M + 1:
            bt1temp = bt1.copy()
            interpBt1 = interp1d( np.linspace( 0.0 , 1.0 , bt1.shape[0] ) , bt1temp , axis = 0 )
            bt1 = interpBt1( np.linspace( 0.0 , 1.0 , config.M + 1 ) )

        if not bt1.shape[1] == config.N + 1:
            bt1temp = bt1.copy()
            interpBt1 = interp1d( np.linspace( 0.0 , 1.0 , bt1.shape[1] ) , bt1temp , axis = 1 )
            bt1 = interpBt1( np.linspace( 0.0 , 1.0 , config.N + 1 ) )

    temporalBoundaries = grid.TemporalBoundaries( config.M , config.N , config.P , bt0 , bt1 )

    if not config.dynamics == 0:
        spatialBoundaries = grid.SpatialBoundaries( config.M , config.N , config.P )
        return grid.Boundaries( config.M , config.N , config.P , temporalBoundaries , spatialBoundaries )

    # catching bx from files
    bx0 = arrayFromFile( config.filemx0 )
    bx1 = arrayFromFile( config.filemx1 )

    if bx0 is None or bx1 is None:
        raise IOError('Could not load spatial X boundaries')

    try:
        bx0 = np.array(bx0)
        bx1 = np.array(bx1)
    except:
        raise IOError('Could not cast spatial X boundaries into arrays')

    if len(bx0.shape == 1):
        bx0 = bx0.reshape((config.N+1,config.P+1))

    if len(bx1.shape == 1):
        bx1 = bx1.reshape((config.N+1,config.P+1))

    if ( not len(bx0.shape) == 2 or
         not len(bx1.shape) == 2 ):
        raise IOError('Spatial X boundaries must be 2-dimensional arrays')

    if not bx0.shape == (config.N+1,config.P+1):
        print( 'Interpolating bx0 into OT resolution ...')

        if not bx0.shape[0] == config.N + 1:
            bx0temp = bx0.copy()
            interpBx0 = interp1d( np.linspace( 0.0 , 1.0 , bx0.shape[0] ) , bx0temp , axis = 0 )
            bx0 = interpBx0( np.linspace( 0.0 , 1.0 , config.N + 1 ) )

        if not bx0.shape[1] == config.P + 1:
            bx0temp = bx0.copy()
            interpBx0 = interp1d( np.linspace( 0.0 , 1.0 , bx0.shape[1] ) , bx0temp , axis = 1 )
            bx0 = interpBx0( np.linspace( 0.0 , 1.0 , config.P + 1 ) )

    if not bx1.shape == (config.N+1,config.P+1):
        print( 'Interpolating bx1 into OT resolution ...')

        if not bx1.shape[0] == config.N + 1:
            bx1temp = bx1.copy()
            interpBx1 = interp1d( np.linspace( 0.0 , 1.0 , bx1.shape[0] ) , bx1temp , axis = 0 )
            bx1 = interpBx1( np.linspace( 0.0 , 1.0 , config.N + 1 ) )

        if not bx1.shape[1] == config.P + 1:
            bx1temp = bx1.copy()
            interpBx1 = interp1d( np.linspace( 0.0 , 1.0 , bx1.shape[1] ) , bx1temp , axis = 1 )
            bx1 = interpBx1( np.linspace( 0.0 , 1.0 , config.P + 1 ) )

    # catching by from files
    by0 = arrayFromFile( config.filemy0 )
    by1 = arrayFromFile( config.filemy1 )

    if by0 is None or by1 is None:
        raise IOError('Could not load spatial Y boundaries')

    try:
        by0 = np.array(by0)
        by1 = np.array(by1)
    except:
        raise IOError('Could not cast spatial Y boundaries into arrays')

    if len(by0.shape == 1):
        by0 = by0.reshape((config.M+1,config.P+1))

    if len(by1.shape == 1):
        by1 = by1.reshape((config.M+1,config.P+1))

    if ( not len(by0.shape) == 2 or
         not len(by1.shape) == 2 ):
        raise IOError('Spatial Y boundaries must be 2-dimensional arrays')

    if not by0.shape == (config.M+1,config.P+1):
        print( 'Interpolating by0 into OT resolution ...')

        if not by0.shape[0] == config.M + 1:
            by0temp = by0.copy()
            interpBy0 = interp1d( np.linspace( 0.0 , 1.0 , by0.shape[0] ) , by0temp , axis = 0 )
            by0 = interpBy0( np.linspace( 0.0 , 1.0 , config.M + 1 ) )

        if not by0.shape[1] == config.P + 1:
            by0temp = by0.copy()
            interpBy0 = interp1d( np.linspace( 0.0 , 1.0 , by0.shape[1] ) , by0temp , axis = 1 )
            by0 = interpBy0( np.linspace( 0.0 , 1.0 , config.P + 1 ) )

    if not by1.shape == (config.M+1,config.P+1):
        print( 'Interpolating by1 into OT resolution ...')

        if not by1.shape[0] == config.M + 1:
            by1temp = by1.copy()
            interpBy1 = interp1d( np.linspace( 0.0 , 1.0 , by1.shape[0] ) , by1temp , axis = 0 )
            by1 = interpBy1( np.linspace( 0.0 , 1.0 , config.M + 1 ) )

        if not by1.shape[1] == config.P + 1:
            by1temp = by1.copy()
            interpBy1 = interp1d( np.linspace( 0.0 , 1.0 , by1.shape[1] ) , by1temp , axis = 1 )
            by1 = interpBy1( np.linspace( 0.0 , 1.0 , config.P + 1 ) )

    spatialBoundaries = grid.SpatialBoundaries( config.M , config.N , config.P , bx0 , bx1 , by0 , by1 )
    
    return grid.Boundaries( config.M , config.N , config.P , temporalBoundaries , spatialBoundaries )
