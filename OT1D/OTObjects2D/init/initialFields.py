##################
# initialFields.py
##################
#
# defines initial fields for a given configuration
#

import numpy as np
from ..grid import grid

def initialStaggeredField(config):
    mx = np.zeros(shape=(config.M+2,config.N+1,config.P+1))
    my = np.zeros(shape=(config.M+1,config.N+2,config.P+1))
    f  = np.zeros(shape=(config.M+1,config.N+1,config.P+2))

    if config.dynamics == 0:

        for i in xrange(config.P+2):
            t = float(i)/(config.P+1.)
            f[:,:,i] = ( config.boundaries.temporalBoundaries.bt0[:,:] * ( 1. - t ) + 
                         config.boundaries.temporalBoundaries.bt1[:,:] * t )

        massIncomingX = ( ( float(config.M) / float(config.P) ) * 
                          np.cumsum( config.boundaries.spatialBoundaries.bx0 - 
                                     config.boundaries.spatialBoundaries.bx1 , axis = 1 ) )

        for i in xrange(config.P+1):
            for j in xrange(config.N+1):
                f[:,j,i+1] += massIncomingX[j,i] / ( config.M + 1. )

        massIncomingY = ( ( float(config.N) / float(config.P) ) * 
                          np.cumsum( config.boundaries.spatialBoundaries.by0 - 
                                     config.boundaries.spatialBoundaries.by1 , axis = 1 ) )

        for i in xrange(config.P+1):
            for j in xrange(config.M+1):
                f[j,:,i+1] += massIncomingY[j,i] / ( config.N + 1. )

    else:
    
        for i in xrange(config.P+2):
            t = float(i)/(config.P+1.)
            f[:,:,i] = ( config.boundaries.temporalBoundaries.bt0[:,:] * ( 1. - t ) +
                         config.boundaries.temporalBoundaries.bt1[:,:] * t )
            
    return grid.StaggeredField( config.M , config.N , config.P ,
                                mx , my, f )

def initialCenteredField(config):
    return initialStaggeredField(config).interpolation()

def initialStaggeredCenteredField(config):
    staggeredField = initialStaggeredField(config)
    return grid.StaggeredCenteredField( config.M , config.N , config.P ,
                                        staggeredField , staggeredField.interpolation() )
