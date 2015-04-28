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


