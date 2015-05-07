####################
# defineProximals.py
####################
#
# Selects correct proximal operators for the given configuration
#
# config must define :
#   * N
#   * P
#   * dynamics
#   * boundaries
#

from ..grid import grid

from proximalJ import ProxJ

from div.proxCdiv import ProxCdiv
from div.proxCdivb import ProxCdivb
from div.proxCdivtb import ProxCdivtb

from sc.proxCsc import ProxCsc
from sc.proxCscb import ProxCscb
from sc.proxCsctb import ProxCsctb
from sc.proxCscrb import ProxCscrb

from bound.proxCb import ProxCb
from bound.proxCtb import ProxCtb
from bound.proxCrb import ProxCrb

def proximalForConfig(config):

    if config.dynamics == 0 or config.dynamics == 1:
        # normal dynamics
        proxCdiv = ProxCdivb( config.M , config.N , config.P ,
                              grid.DivergenceBoundaries( config.M , config.N , config.P , boundaries=config.boundaries) )

        proxCsc  = ProxCscb( config.M , config.N , config.P ,
                             grid.CenteredFieldBoundaries( config.M , config.N , config.P , boundaries=config.boundaries) )

        proxJ    = ProxJ( config.M , config.N , config.P )

        proxCb   = ProxCb( config.M , config.N, config.P, config.boundaries )

    elif config.dynamics == 2:
        # no contrain for m
        proxCdiv = ProxCdivtb( config.M , config.N , config.P ,
                               grid.DivergenceTemporalBoundaries( config.M , config.N , config.P , 
                                                                  temporalBoundaries=config.boundaries.temporalBoundaries ) )
        
        proxCsc  = ProxCsctb( config.M , config.N , config.P ,
                              grid.CenteredFieldTemporalBoundaries( config.M , config.N , config.P , 
                                                                    temporalBoundaries=config.boundaries.temporalBoundaries ) )

        proxJ    = ProxJ( config.M , config.N , config.P )

        proxCb   = ProxCtb( config.M , config.N , config.P ,
                            config.boundaries.temporalBoundaries )

    elif config.dynamics == 3:
        # reservoir
        # for Adr
        proxCdiv = ProxCdiv( config.M , config.N , config.P )

        proxCsc  = ProxCscrb( config.M , config.N , config.P ,
                              grid.CenteredFieldBoundaries( config.M , config.N ,config.P , boundaries=config.boundaries ) )

        proxJ    = ProxJ( config.M , config.N , config.P )

        proxCb   = ProxCrb( config.M , config.N , config.P ,
                            config.boundaries )

    elif config.dynamics == 4:
        # reservoir
        # for Adr 3

        proxCdiv = ProxCdiv( config.M , config.N , config.P )

        proxCsc  = ProxCsc( config.M , config.N, config.P )

        proxJ    = ProxJ( config.M , config.N , config.P )

        proxCb   = ProxCrb( config.M , config.N , config.P ,
                            config.boundaries )

    return proxCdiv,proxCsc,proxJ,proxCb

def testProximals(M, N, P, nTest):

    maxError = 0.

    print('__________________________________________________')
    print('Testing proximal operators...')
    print('M     = '+str(M))
    print('N     = '+str(N))
    print('P     = '+str(P))
    print('nTest = '+str(nTest))

    print('__________________________________________________')
    print('Testing ProxCb...')
    kernel = grid.Boundaries.random(M,N,P)
    prox   = ProxCb(M,N,P,kernel)
    e = prox.test(nTest,overwrite=False)
    print('mean error = '+str(e))
    print('timing     : '+str(prox.timing(nTest,overwrite=False)))

    maxError = max( maxError , e )

    print('__________________________________________________')
    print('Testing ProxCtb...')
    kernel = grid.TemporalBoundaries.random(M,N,P)
    prox   = ProxCtb(M,N,P,kernel)
    e = prox.test(nTest,overwrite=False)
    print('mean error = '+str(e))
    print('timing     : '+str(prox.timing(nTest,overwrite=False)))

    maxError = max( maxError , e )

    print('__________________________________________________')
    print('Testing ProxCrb...')
    kernel = grid.Boundaries.random(M,N,P)
    prox   = ProxCrb(M,N,P,kernel)
    e = prox.test(nTest,overwrite=False)
    print('mean error = '+str(e))
    print('timing     : '+str(prox.timing(nTest,overwrite=False)))

    maxError = max( maxError , e )

    print('__________________________________________________')
    print('Testing ProxCdiv...')
    kernel = grid.Divergence.random(M,N,P)
    prox   = ProxCdiv(M,N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCdivb...')
    kernel = grid.DivergenceBoundaries.random(M,N,P)
    kernel.correctMassDefault(1.e-8)
    prox   = ProxCdivb(M,N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCdivtb...')
    kernel = grid.DivergenceTemporalBoundaries.random(M,N,P)
    prox   = ProxCdivtb(M,N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCsc...')
    kernel = grid.CenteredField.random(M,N,P)
    prox   = ProxCsc(M,N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCscb...')
    kernel = grid.CenteredFieldBoundaries.random(M,N,P)
    prox   = ProxCscb(M,N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCsctb...')
    kernel = grid.CenteredFieldTemporalBoundaries.random(M,N,P)
    prox   = ProxCsctb(M,N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCscrb...')
    kernel = grid.CenteredFieldBoundaries.random(M,N,P)
    kernel.boundaries.temporalBoundaries.bt1[0,:] = 0.
    kernel.boundaries.temporalBoundaries.bt1[M,:] = 0.
    kernel.boundaries.temporalBoundaries.bt1[:,0] = 0.
    kernel.boundaries.temporalBoundaries.bt1[:,N] = 0.
    prox   = ProxCscrb(M,N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Finished testing proximal operators')
    print('max error : '+str(maxError))
    print('__________________________________________________')
