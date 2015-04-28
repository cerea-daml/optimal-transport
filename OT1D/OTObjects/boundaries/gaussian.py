#############
# gaussian.py
#############
#
# defines some possible boundary conditions
#

import numpy as np
from ..grid import grid

def boundaryGaussian(N,P,
                     A0,alphaX0,x0,
                     A1,alphaX1,x1):
    #
    # f0(x) = A0exp(-alphaX0(x-x0)^2)
    # f1(x) = A1exp(-alphaX1(x-x1)^2)
    #

    # Normalize parameters
    x0n = np.mod(x0,1.)*N
    x1n = np.mod(x1,1.)*N
    alphaX0n = alphaX0/(N*N)
    alphaX1n = alphaX1/(N*N)

    # Defines f0 and f1
    X  = np.arange(N+1)

    f0 = A0 * np.exp( -alphaX0n * np.power( X - x0n , 2 ) )
    f1 = A1 * np.exp( -alphaX1n * np.power( X - x1n , 2 ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def boundaryGaussian2(N,P,
                      A00,A01,alphaX00,alphaX01,x00,x01,
                      A10,A11,alphaX10,alphaX11,x10,x11)
    #
    # f0(x) = A00exp(-alphaX00(x-x00)^2) + A01exp(-alphaX01(x-x01)^2)
    # f1(x) = A10exp(-alphaX10(x-x10)^2) + A11exp(-alphaX11(x-x11)^2)
    #

    # Normalize parameters
    x00n = np.mod(x00,1.)*N
    x01n = np.mod(x01,1.)*N
    x10n = np.mod(x10,1.)*N
    x11n = np.mod(x11,1.)*N

    alphaX00n = alphaX00/(N*N)
    alphaX01n = alphaX01/(N*N)
    alphaX10n = alphaX10/(N*N)
    alphaX11n = alphaX11/(N*N)

    # Defines f0 and f1
    X  = np.arange(N+1)

    f0 = ( A00 * np.exp( -alphaX00n * np.power( X - x00n , 2 ) ) +
           A01 * np.exp( -alphaX01n * np.power( X - x01n , 2 ) ) )

    f1 = ( A10 * np.exp( -alphaX10n * np.power( X - x10n , 2 ) ) +
           A11 * np.exp( -alphaX11n * np.power( X - x11n , 2 ) ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def defaultBoundaryGaussian(N, P):
    A0 = 1.
    alphaX0 = N*N*0.05
    x0 = 0.375
        
    A1 = 1.
    alphaX1 = N*N*0.05
    x1 = 0.625

    return boundaryGaussian(N,P,
                            A0,alphaX0,x0,A1,alphaX1,x1)

def defaultBoundaryGaussian2(N, P):
    A00 = 1.
    A01 = 1.
    alphaX00 = N*N*0.25
    alphaX01 = N*N*0.25
    x00 = 0.25
    x01 = 0.5
    
    A10 = 1.
    A11 = 1.
    alphaX10 = N*N*0.25
    alphaX11 = N*N*0.25
    x10 = 0.5
    x11 = 0.75
    
    return boundaryGaussian2(N,P,
                             A00,A01,alphaX00,alphaX01,x00,x01,
                             A10,A11,alphaX10,alphaX11,x10,x11)
