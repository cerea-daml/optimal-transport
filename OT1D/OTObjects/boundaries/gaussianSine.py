#################
# gaussianSine.py
#################
#
# defines some possible boundary conditions
#

import numpy as np
from ..grid import grid

def boundaryGaussianSine(N,P,
                         A0,alphaX0,betaX0,x00,x01,
                         A1,alphaX1,betaX1,x10,x11):
    #
    # f0 = A0exp(-alphaX0(x-x00)^2)sin^2(betaX0(x-x01))
    # f1 = A1exp(-alphaX1(x-x10)^2)sin^2(betaX1(x-x11))
    #

    # Normalize parameters
    x00n = np.mod(x00,1.)*N
    x01n = np.mod(x01,1.)*N
    x10n = np.mod(x10,1.)*N
    x11n = np.mod(x11,1.)*N

    alphaX0n = alphaX0/(N*N)
    alphaX1n = alphaX1/(N*N)
    betaX0n = betaX0/N
    betaX1n = betaX1/N

    # Defines f0 and f1
    X  = np.arange(N+1)

    f0  = ( A0 * np.exp( -alphaX0n * np.power( X - x00n , 2 ) ) *
            np.power( np.sin( betaX0n * ( X - x01n ) ) , 2 ) )

    f1  = ( A1 * np.exp( -alphaX1n * np.power( X - x10n , 2 ) ) * 
            np.power( np.sin( betaX1n * ( X - x11n ) ) , 2 ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def boundaryGaussianCosine(N,P,
                           A0,alphaX0,betaX0,x00,x01,
                           A1,alphaX1,betaX1,x10,x11):
    #
    # f0 = A0exp(-alphaX0(x-x00)^2)cos^2(betaX0(x-x01))
    # f1 = A1exp(-alphaX1(x-x10)^2)cos^2(betaX1(x-x11))
    #

    # Normalize parameters
    x00n = np.mod(x00,1.)*N
    x01n = np.mod(x01,1.)*N
    x10n = np.mod(x10,1.)*N
    x11n = np.mod(x11,1.)*N

    alphaX0n = alphaX0/(N*N)
    alphaX1n = alphaX1/(N*N)
    betaX0n = betaX0/N
    betaX1n = betaX1/N

    # Defines f0 and f1
    X  = np.arange(N+1)

    f0  = ( A0 * np.exp( -alphaX0n * np.power( X - x00n , 2 ) ) *
            np.power( np.cos( betaX0n * ( X - x01n ) ) , 2 ) )

    f1  = ( A1 * np.exp( -alphaX1n * np.power( X - x10n , 2 ) ) *
            np.power( np.cos( betaX1n * ( X - x11n ) ) , 2 ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def defaultBoundaryGaussianSine(N, P):
    A0 = 1.
    alphaX0 = N*N*0.05
    betaX0 = 16*np.pi
    x00 = 0.25
    x01 = 0.
            
    A1 = 1.
    alphaX1 = N*N*0.05
    betaX1 = 16*np.pi
    x10 = 0.75
    x11 = 0.
    
    return boundaryGaussianSine(N,P,
                                A0,alphaX0,betaX0,x00,x01,
                                A1,alphaX1,betaX1,x10,x11)

def defaultBoundaryGaussianCosine(N, P):
    A0 = 1.
    alphaX0 = N*N*0.05
    betaX0 = 16*np.pi
    x00 = 0.25
    x01 = 0.
            
    A1 = 1.
    alphaX1 = N*N*0.05
    betaX1 = 16*np.pi
    x10 = 0.75
    x11 = 0.
    
    return boundaryGaussianCosine(N,P,
                                  A0,alphaX0,betaX0,x00,x01,
                                  A1,alphaX1,betaX1,x10,x11)
