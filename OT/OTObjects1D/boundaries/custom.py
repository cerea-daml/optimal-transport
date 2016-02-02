#############
# cutom.py
#############
#
# defines some possible boundary conditions
#

import numpy as np
from ..grid import grid

def customBoundary(N,P):

    X  = np.linspace( 0.0 , 1.0 , N + 1 )

    f0 = ( 0.1 + 
           np.exp( - 60. * np.power( X - 0.75 , 2 ) ) )
    
    f1 = ( 0.1 + 
           0.5 * np.exp( - 260. * np.power(X - 0.2 , 2 ) ) +
           0.5 * np.exp( - 260. * np.power(X - 0.4 , 2 ) ) )
 
    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def customBoundaryRev(N,P):

    X  = np.linspace( 0.0 , 1.0 , N + 1 )

    f1 = ( 0.1 + 
           np.exp( - 60. * np.power( X - 0.75 , 2 ) ) )
    
    f0 = ( 0.1 + 
           0.5 * np.exp( - 260. * np.power(X - 0.2 , 2 ) ) +
           0.5 * np.exp( - 260. * np.power(X - 0.4 , 2 ) ) )
 
    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )
