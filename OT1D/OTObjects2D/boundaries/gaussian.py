#############
# gaussian.py
#############
#
# defines some possible boundary conditions
#

import numpy as np
from ..grid import grid

def boundaryGaussian(M,N,P,
                     A0,alphaX0,alphaY0,x0,y0,
                     A1,alphaX1,alphaY1,x1,y1):
    #
    # f0(x) = A0exp(-alphaX0(x-x0)^2)exp(-alphaY0(y-y0)^2)
    # f1(x) = A1exp(-alphaX1(x-x1)^2)exp(-alphaY1(y-y0)^2)
    #

    x0 = np.mod(x0,1.)
    x1 = np.mod(x1,1.)
    y0 = np.mod(y0,1.)
    y1 = np.mod(y1,1.)

    # Defines f0 and f1
    x   = np.linspace( 0.0 , 1.0 , M + 1 )
    y   = np.linspace( 0.0 , 1.0 , N + 1 ) 
    X,Y = np.meshgrid( x , y , indexing='ij' )

    f0  = A0 * np.exp( -alphaX0 * np.power( X - x0 , 2 ) ) * np.exp( -alphaY0 * np.power( Y - y0 , 2 ) )
    f1  = A1 * np.exp( -alphaX1 * np.power( X - x1 , 2 ) ) * np.exp( -alphaY1 * np.power( Y - y1 , 2 ) )

    temporalBoundaries = grid.TemporalBoundaries( M , N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( M , N , P )

    return grid.Boundaries( M , N , P ,
                            temporalBoundaries, spatialBoundaries )

def boundaryGaussian2(M,N,P,
                      A00,A01,alphaX00,alphaX01,alphaY00,alphaY01,x00,x01,y00,y01,
                      A10,A11,alphaX10,alphaX11,alphaY10,alphaY11,x10,x11,y10,y11):
    #
    # f0(x) = A00exp(-alphaX00(x-x00)^2)exp(-alphaY00(x-y00)^2) + A01exp(-alphaX01(x-x01)^2)exp(-alphaY01(x-y01)^2)
    # f1(x) = A10exp(-alphaX10(x-x10)^2)exp(-alphaY10(x-y10)^2) + A11exp(-alphaX11(x-x11)^2)exp(-alphaY11(x-y11)^2)
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
    X,Y = np.meshgrid( x , y , indexing='ij')

    f0 = ( A00 * np.exp( -alphaX00 * np.power( X - x00 , 2 ) ) * np.exp( -alphaY00 * np.power( Y - y00 , 2 ) ) +
           A01 * np.exp( -alphaX01 * np.power( X - x01 , 2 ) ) * np.exp( -alphaY01 * np.power( Y - y01 , 2 ) ) )

    f1 = ( A10 * np.exp( -alphaX10 * np.power( X - x10 , 2 ) ) * np.exp( -alphaY10 * np.power( Y - y10 , 2 ) ) +
           A11 * np.exp( -alphaX11 * np.power( X - x11 , 2 ) ) * np.exp( -alphaY11 * np.power( Y - y11 , 2 ) ) )

    temporalBoundaries = grid.TemporalBoundaries( M , N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( M , N , P )

    return grid.Boundaries( M , N , P ,
                            temporalBoundaries, spatialBoundaries )

def defaultBoundaryGaussian(M, N, P):
    A0      = 1.
    alphaX0 = 60.
    alphaY0 = 60.
    x0      = 0.375
    y0      = 0.375
        
    A1      = 1.
    alphaX1 = 60.
    alphaY1 = 60.
    x1      = 0.625
    y1      = 0.625

    return boundaryGaussian(M,N,P,
                            A0,alphaX0,alphaY0,x0,y0,
                            A1,alphaX1,alphaY1,x1,y1)

def defaultBoundaryGaussian2(M, N, P):
    A00      = 1.
    A01      = 1.
    alphaX00 = 260.
    alphaX01 = 260.
    x00      = 0.25
    x01      = 0.5
    alphaY00 = 260.
    alphaY01 = 260.
    y00      = 0.25
    y01      = 0.5
    
    A10      = 1.
    A11      = 1.
    alphaX10 = 260.
    alphaX11 = 260.
    x10      = 0.5
    x11      = 0.75
    alphaY10 = 260.
    alphaY11 = 260.
    y10      = 0.5
    y11      = 0.75

    return boundaryGaussian2(M,N,P,
                             A00,A01,alphaX00,alphaX01,alphaY00,alphaY01,x00,x01,y00,y01,
                             A10,A11,alphaX10,alphaX11,alphaY10,alphaY11,x10,x11,y10,y11)
