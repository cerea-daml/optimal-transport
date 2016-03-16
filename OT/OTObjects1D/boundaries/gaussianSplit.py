#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

##################
# gaussianSplit.py
##################
#
# defines some possible boundary conditions
#

import numpy as np
from ..grid import grid

def boundaryGaussianSplit1(N,P,
                           A00,A01,alphaX00,alphaX01,x00,x01,
                           A1,alphaX1,x1):
    #
    # f0(x) = A00exp(-alphaX00(x-x00)^2) + A01exp(-alphaX01(x-x01)^2)
    # f1(x) = A1exp(-alphaX1(x-x1)^2)
    #

    x1  = np.mod(x1,1.)
    x00 = np.mod(x00,1.)
    x01 = np.mod(x01,1.)

    # Defines f0 and f1
    X  = np.linspace( 0.0 , 1.0 , N + 1 )
    
    f0 = ( A00 * np.exp( -alphaX00 * np.power( X - x00 , 2 ) ) +
           A01 * np.exp( -alphaX01 * np.power( X - x01 , 2 ) ) )

    f1 = ( A1  * np.exp( -alphaX1  * np.power( X - x1  , 2 ) ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def boundaryGaussianSplit2(N,P,
                           A0,alphaX0,x0,
                           A10,A11,alphaX10,alphaX11,x10,x11):
    #
    # f0(x) = A0exp(-alphaX0(x-x0)^2) 
    # f1(x) = A10exp(-alphaX10(x-x10)^2) + A11exp(-alphaX11(x-x11)^2)
    #

    x0  = np.mod(x0,1.)
    x10 = np.mod(x10,1.)
    x11 = np.mod(x11,1.)

    # Defines f0 and f1
    X  = np.linspace( 0.0 , 1.0 , N + 1 )

    f0 = ( A0  * np.exp( -alphaX0  * np.power( X - x0  , 2 ) ) )
    f1 = ( A10 * np.exp( -alphaX10 * np.power( X - x10 , 2 ) ) +
           A11 * np.exp( -alphaX11 * np.power( X - x11 , 2 ) ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def defaultBoundaryGaussianSplit1(N, P):
    A00      = 1.
    A01      = 1.
    alphaX00 = 110.
    alphaX01 = 110.
    x00      = 0.25
    x01      = 0.75
        
    A1       = 1.
    alphaX1  = 60.
    x1       = 0.5
    
    return boundaryGaussianSplit1(N, P,
                                  A00,A01,alphaX00,alphaX01,x00,x01,
                                  A1,alphaX1,x1)

def defaultBoundaryGaussianSplit2(N, P):
    A0       = 1.
    alphaX0  = 60.
    x0       = 0.5

    A10      = 1.
    A11      = 1.
    alphaX10 = 110.
    alphaX11 = 110.
    x10      = 0.25
    x11      = 0.75
        
    return boundaryGaussianSplit2(N, P,
                                  A0,alphaX0,x0,
                                  A10,A11,alphaX10,alphaX11,x10,x11)
