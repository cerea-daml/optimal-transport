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
#   * gamma (for ProxJ)
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

    if config.dynamics == 0:
        # normal dynamics
        proxCdiv = ProxCdivb( config.N , config.P ,
                              grid.DivergenceBoundaries( config.N , config.P , boundaries=config.boundaries) )

        proxCsc  = ProxCscb( config.N , config.P ,
                             grid.CenteredFieldBoundaries( config.N , config.P , boundaries=config.boundaries) )

        proxJ    = ProxJ( config.N , config.P , config.gamma )

        proxCb   = ProxCb( config.N, config.P, config.boundaries )

    elif config.dynamics == 1:
        # no contrain for m
        proxCdiv = ProxCdivtb( config.N , config.P ,
                               grid.DivergenceTemporalBoundaries( config.N , config.P , temporalBoundaries=config.boundaries.temporalBoundaries ) )
        
        proxCsc  = ProxCsctb( config.N , config.P ,
                              grid.CenteredFieldTemporalBoundaries( config.N , config.P , temporalBoundaries=config.boundaries.temporalBoundaries ) )

        proxJ    = ProxJ( config.N , config.P , config.gamma )

        proxCb   = ProxCtb( config.N , config.P ,
                            config.boundaries.temporalBoundaries )

    elif config.dynamics == 2:
        # reservoir
        # for Adr
        proxCdiv = ProxCdiv( config.N , config.P )

        proxCsc  = ProxCscrb( config.N , config.P ,
                              grid.CenteredFieldBoundaries( config.N ,config.P , boundaries=config.boundaries ) )

        proxJ    = ProxJ( config.N , config.P , config.gamma )

        proxCb   = ProxCrb( config.N , config.P ,
                            config.boundaries )

    elif config.dynamics == 3:
        # reservoir
        # for Adr 3

        proxCdiv = ProxCdiv( config.N , config.P )

        proxCsc  = ProxCsc( config.N, config.P )

        proxJ    = ProxJ( config.N , config.P , config.gamma )

        proxCb   = ProxCrb( config.N , config.P ,
                            config.boundaries )

    return proxCdiv,proxCsc,proxJ,proxCb

def testProximals(N, P, nTest):

    maxError = 0.

    print('__________________________________________________')
    print('Testing proximal operators...')
    print('N     = '+str(N))
    print('P     = '+str(P))
    print('nTest = '+str(nTest))

    print('__________________________________________________')
    print('Testing ProxCb...')
    kernel = grid.Boundaries.random(N,P)
    prox   = ProxCb(N,P,kernel)
    e = prox.test(nTest,overwrite=False)
    print('mean error = '+str(e))
    print('timing     : '+str(prox.timing(nTest,overwrite=False)))

    maxError = max( maxError , e )

    print('__________________________________________________')
    print('Testing ProxCtb...')
    kernel = grid.TemporalBoundaries.random(N,P)
    prox   = ProxCtb(N,P,kernel)
    e = prox.test(nTest,overwrite=False)
    print('mean error = '+str(e))
    print('timing     : '+str(prox.timing(nTest,overwrite=False)))

    maxError = max( maxError , e )

    print('__________________________________________________')
    print('Testing ProxCrb...')
    kernel = grid.Boundaries.random(N,P)
    prox   = ProxCrb(N,P,kernel)
    e = prox.test(nTest,overwrite=False)
    print('mean error = '+str(e))
    print('timing     : '+str(prox.timing(nTest,overwrite=False)))

    maxError = max( maxError , e )

    print('__________________________________________________')
    print('Testing ProxCdiv...')
    kernel = grid.Divergence.random(N,P)
    prox   = ProxCdiv(N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCdivb...')
    kernel = grid.DivergenceBoundaries.random(N,P)
    kernel.correctMassDefault(1.e-8)
    prox   = ProxCdivb(N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCdivtb...')
    kernel = grid.DivergenceTemporalBoundaries.random(N,P)
    prox   = ProxCdivtb(N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCsc...')
    kernel = grid.CenteredField.random(N,P)
    prox   = ProxCsc(N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCscb...')
    kernel = grid.CenteredFieldBoundaries.random(N,P)
    prox   = ProxCscb(N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCsctb...')
    kernel = grid.CenteredFieldTemporalBoundaries.random(N,P)
    prox   = ProxCsctb(N,P,kernel)
    e1 = prox.testInverse(nTest)
    e2 = prox.test(nTest)
    print('mean error (inverse) = '+str(e1))
    print('mean error (kernel)  = '+str(e2))
    print('timing               : '+str(prox.timing(nTest)))

    maxError = max( max( maxError , e1 ) , e2 )

    print('__________________________________________________')
    print('Testing ProxCscrb...')
    kernel = grid.CenteredFieldBoundaries.random(N,P)
    kernel.boundaries.temporalBoundaries.bt1[0] = 0.
    kernel.boundaries.temporalBoundaries.bt1[N] = 0.
    prox   = ProxCscrb(N,P,kernel)
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
