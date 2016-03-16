#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
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

    x00 = np.mod(x00,1.)
    x01 = np.mod(x01,1.)
    x10 = np.mod(x10,1.)
    x11 = np.mod(x11,1.)

    # Defines f0 and f1
    X  = np.linspace( 0.0 , 1.0 , N + 1 )

    f0 = ( A0 * np.exp( -alphaX0 * np.power( X - x00 , 2 ) ) *
           np.power( np.sin( betaX0 * ( X - x01 ) ) , 2 ) )

    f1 = ( A1 * np.exp( -alphaX1 * np.power( X - x10 , 2 ) ) * 
           np.power( np.sin( betaX1 * ( X - x11 ) ) , 2 ) )

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

    x00 = np.mod(x00,1.)
    x01 = np.mod(x01,1.)
    x10 = np.mod(x10,1.)
    x11 = np.mod(x11,1.)

    # Defines f0 and f1
    X  = np.linspace( 0.0 , 1.0 , N + 1 )

    f0 = ( A0 * np.exp( -alphaX0 * np.power( X - x00 , 2 ) ) *
           np.power( np.cos( betaX0 * ( X - x01 ) ) , 2 ) )

    f1 = ( A1 * np.exp( -alphaX1 * np.power( X - x10 , 2 ) ) *
           np.power( np.cos( betaX1 * ( X - x11 ) ) , 2 ) )

    temporalBoundaries = grid.TemporalBoundaries( N , P , f0 , f1 )
    spatialBoundaries  = grid.SpatialBoundaries( N , P )

    return grid.Boundaries( N , P ,
                            temporalBoundaries, spatialBoundaries )

def defaultBoundaryGaussianSine(N, P):
    A0      = 1.
    alphaX0 = 60.
    betaX0  = 16*np.pi
    x00     = 0.25
    x01     = 0.
            
    A1      = 1.
    alphaX1 = 60.
    betaX1  = 16*np.pi
    x10     = 0.75
    x11     = 0.
    
    return boundaryGaussianSine(N,P,
                                A0,alphaX0,betaX0,x00,x01,
                                A1,alphaX1,betaX1,x10,x11)

def defaultBoundaryGaussianCosine(N, P):
    A0      = 1.
    alphaX0 = 60.
    betaX0  = 16*np.pi
    x00     = 0.25
    x01     = 0.
            
    A1      = 1.
    alphaX1 = 60.
    betaX1  = 16*np.pi
    x10     = 0.75
    x11     = 0.
    
    return boundaryGaussianCosine(N,P,
                                  A0,alphaX0,betaX0,x00,x01,
                                  A1,alphaX1,betaX1,x10,x11)
