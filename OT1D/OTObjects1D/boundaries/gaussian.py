#############
# gaussian.py
#############
#
# defines some possible boundary conditions
#

import numpy as np

from ..grid          import grid
from ...utils.extent import xExtent

def boundaryGaussian(N,P,
                     A0,alphaX0,x0,
                     A1,alphaX1,x1):
    #
    # f0(x) = A0exp(-alphaX0(x-x0)^2)
    # f1(x) = A1exp(-alphaX1(x-x1)^2)
    #

    x0 = np.mod(x0,1.)
    x1 = np.mod(x1,1.)

    # Defines f0 and f1
    X  = xExtent(N)

    f0 = A0 * np.exp( -alphaX0 * np.power( X - x0 , 2 ) )
    f1 = A1 * np.exp( -alphaX1 * np.power( X - x1 , 2 ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def boundaryGaussian2(N,P,
                      A00,A01,alphaX00,alphaX01,x00,x01,
                      A10,A11,alphaX10,alphaX11,x10,x11):
    #
    # f0(x) = A00exp(-alphaX00(x-x00)^2) + A01exp(-alphaX01(x-x01)^2)
    # f1(x) = A10exp(-alphaX10(x-x10)^2) + A11exp(-alphaX11(x-x11)^2)
    #

    x00 = np.mod(x00,1.)
    x01 = np.mod(x01,1.)
    x10 = np.mod(x10,1.)
    x11 = np.mod(x11,1.)

    # Defines f0 and f1
    X  = xExtent(N)

    f0 = ( A00 * np.exp( -alphaX00 * np.power( X - x00 , 2 ) ) +
           A01 * np.exp( -alphaX01 * np.power( X - x01 , 2 ) ) )

    f1 = ( A10 * np.exp( -alphaX10 * np.power( X - x10 , 2 ) ) +
           A11 * np.exp( -alphaX11 * np.power( X - x11 , 2 ) ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def defaultBoundaryGaussian(N, P):
    A0      = 1.
    alphaX0 = 60.
    x0      = 0.375
        
    A1      = 1.
    alphaX1 = 60.
    x1      = 0.625

    return boundaryGaussian(N,P,
                            A0,alphaX0,x0,A1,alphaX1,x1)

def defaultBoundaryGaussian2(N, P):
    A00      = 1.
    A01      = 1.
    alphaX00 = 260.
    alphaX01 = 260.
    x00      = 0.25
    x01      = 0.5
    
    A10      = 1.
    A11      = 1.
    alphaX10 = 260.
    alphaX11 = 260.
    x10      = 0.5
    x11      = 0.75
    
    return boundaryGaussian2(N,P,
                             A00,A01,alphaX00,alphaX01,x00,x01,
                             A10,A11,alphaX10,alphaX11,x10,x11)
