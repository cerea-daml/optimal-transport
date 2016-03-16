#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
##################
# initialFields.py
##################
#
# defines initial fields for a given configuration
#
# config must define :
#   * N
#   * P
#   * boundaries
#   * dynamics
#

import numpy as np
from ..grid import grid

def initialStaggeredField(config):
    m = np.zeros(shape=(config.N+2,config.P+1))
    f = np.zeros(shape=(config.N+1,config.P+2))

    if config.dynamics == 0 or config.dynamics == 1:

        for i in xrange(config.P+2):
            t = float(i)/(config.P+1.)
            f[:,i] = ( config.boundaries.temporalBoundaries.bt0[:] * ( 1. - t ) + 
                       config.boundaries.temporalBoundaries.bt1[:] * t )

        massIncoming = ( ( float(config.N) / float(config.P) ) * 
                         np.cumsum( config.boundaries.spatialBoundaries.bx0 - 
                                    config.boundaries.spatialBoundaries.bx1 ) )

        for i in xrange(config.P+1):
            f[:,i+1] += massIncoming[i] / ( config.N + 1. )

    else:
    
        for i in xrange(config.P+2):
            t = float(i)/(config.P+1.)
            f[:,i] = ( config.boundaries.temporalBoundaries.bt0[:] * ( 1. - t ) +
                       config.boundaries.temporalBoundaries.bt1[:] * t )
            
    return grid.StaggeredField( config.N , config.P ,
                                m , f )

def initialCenteredField(config):
    return initialStaggeredField(config).interpolation()

def initialStaggeredCenteredField(config):
    staggeredField = initialStaggeredField(config)
    return grid.StaggeredCenteredField( config.N , config.P ,
                                        staggeredField , staggeredField.interpolation() )
