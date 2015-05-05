#################
# gaussianSine.py
#################
#
# defines some possible boundary conditions
#

import numpy as np
from ..grid import grid

def boundaryGaussianSine(M,N,P,
                         A0,alphaX0,betaX0,alphaY0,betaY0,x00,x01,y00,y01,
                         A1,alphaX1,betaX1,alphaY1,betaY1,x10,x11,y10,y11)
    #
    # f0 = A0exp(-alphaX0(x-x00)^2)exp(-alphaY0(y-y00)^2)sin^2(betaX0(x-x01))sin^2(betaY0(y-y01))
    # f1 = A1exp(-alphaX1(x-x10)^2)exp(-alphaY1(y-y10)^2)sin^2(betaX1(x-x11))sin^2(betaY1(y-y11))
    #

    x00 = np.mod(x00,1.)
    x01 = np.mod(x01,1.)
    x10 = np.mod(x10,1.)
    x11 = np.mod(x11,1.)

    y00 = np.mod(y00,1.)
    y01 = np.mod(y01,1.)
    y10 = np.mod(y10,1.)
    y11 = np.mod(y11,1.)

    # Defines f0 and f1
    x   = np.linspace( 0.0 , 1.0 , M + 1 )
    y   = np.linspace( 0.0 , 1.0 , N + 1 )
    X,Y = np.meshgrid( x , y , indexing='ij' )

    f0  = ( A0 * ( np.exp( -alphaX0 * np.power( X - x00 , 2 ) ) * 
                   np.exp( -alphaY0 * np.power( Y - y00 , 2 ) ) *
                   np.power( np.sin( betaX0 * ( X - x01 ) ) , 2 ) * 
                   np.power( np.sin( betaY0 * ( Y - y01 ) ) , 2 ) ) )

    f1  = ( A1 * ( np.exp( -alphaX1 * np.power( X - x10 , 2 ) ) *
                   np.exp( -alphaY1 * np.power( Y - y10 , 2 ) ) *
                   np.power( np.sin( betaX1 * ( X - x11 ) ) , 2 ) *
                   np.power( np.sin( betaY1 * ( Y - y11 ) ) , 2 ) ) )

    temporalBoundaries = grid.TemporalBoundaries( M , N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( M , N , P )

    return grid.Boundaries( M , N , P ,
                            temporalBoundaries, spatialBoundaries )

def boundaryGaussianCosine(M,N,P,
                           A0,alphaX0,betaX0,alphaY0,betaY0,x00,x01,y00,y01,
                           A1,alphaX1,betaX1,alphaY1,betaY1,x10,x11,y10,y11)
    #
    # f0 = A0exp(-alphaX0(x-x00)^2)exp(-alphaY0(y-y00)^2)cos^2(betaX0(x-x01))cos^2(betaY0(y-y01))
    # f1 = A1exp(-alphaX1(x-x10)^2)exp(-alphaY1(y-y10)^2)cos^2(betaX1(x-x11))cos^2(betaY1(y-y11))
    #

    x00 = np.mod(x00,1.)
    x01 = np.mod(x01,1.)
    x10 = np.mod(x10,1.)
    x11 = np.mod(x11,1.)

    y00 = np.mod(y00,1.)
    y01 = np.mod(y01,1.)
    y10 = np.mod(y10,1.)
    y11 = np.mod(y11,1.)

    # Defines f0 and f1
    x   = np.linspace( 0.0 , 1.0 , M + 1 )
    y   = np.linspace( 0.0 , 1.0 , N + 1 )
    X,Y = np.meshgrid( x , y , indexing='ij' )

    f0  = ( A0 * ( np.exp( -alphaX0 * np.power( X - x00 , 2 ) ) * 
                   np.exp( -alphaY0 * np.power( Y - y00 , 2 ) ) *
                   np.power( np.cos( betaX0 * ( X - x01 ) ) , 2 ) * 
                   np.power( np.cos( betaY0 * ( Y - y01 ) ) , 2 ) ) )

    f1  = ( A1 * ( np.exp( -alphaX1 * np.power( X - x10 , 2 ) ) *
                   np.exp( -alphaY1 * np.power( Y - y10 , 2 ) ) *
                   np.power( np.cos( betaX1 * ( X - x11 ) ) , 2 ) *
                   np.power( np.cos( betaY1 * ( Y - y11 ) ) , 2 ) ) )

    temporalBoundaries = grid.TemporalBoundaries( M , N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( M , N , P )

    return grid.Boundaries( M , N , P ,
                            temporalBoundaries, spatialBoundaries )

def defaultBoundaryGaussianSine(M, N, P):
    A0      = 1.
    alphaX0 = 60.
    betaX0  = 16*np.pi
    alphaY0 = 60.
    betaY0  = 16*np.pi
    x00     = 0.25
    x01     = 0.
    y00     = 0.25
    y01     = 0.

    A1      = 1.
    alphaX1 = 60.
    betaX1  = 16*np.pi
    alphaY1 = 60.
    betaY1  = 16*np.pi
    x10     = 0.75
    x11     = 0.
    y10     = 0.75
    y11     = 0.
    return boundaryGaussianSine(M,N,P,
                                A0,alphaX0,betaX0,alphaY0,betaY0,x00,x01,y00,y01,
                                A1,alphaX1,betaX1,alphaY1,betaY1,x10,x11,y10,y11)

def defaultBoundaryGaussianCosine(M, N, P):
    A0      = 1.
    alphaX0 = 60.
    betaX0  = 16*np.pi
    alphaY0 = 60.
    betaY0  = 16*np.pi
    x00     = 0.25
    x01     = 0.
    y00     = 0.25
    y01     = 0.

    A1      = 1.
    alphaX1 = 60.
    betaX1  = 16*np.pi
    alphaY1 = 60.
    betaY1  = 16*np.pi
    x10     = 0.75
    x11     = 0.
    y10     = 0.75
    y11     = 0.
    return boundaryGaussianCosine(M,N,P,
                                  A0,alphaX0,betaX0,alphaY0,betaY0,x00,x01,y00,y01,
                                  A1,alphaX1,betaX1,alphaY1,betaY1,x10,x11,y10,y11)
