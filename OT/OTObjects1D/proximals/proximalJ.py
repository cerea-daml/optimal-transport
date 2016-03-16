#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#############
# Class ProxJ
#############
#
# Proximal operator for the cost function J = sum(m**2/f)
#

import numpy as np
import time as tm

from ..grid import grid
from .. import OTObject as oto

class ProxJ( oto.OTObject ):
    '''
    Proximal operator for the cost function J
    '''

    def __init__(self, N , P):
        oto.OTObject.__init__(self,N,P)

    def __repr__(self):
        return ( 'Proximal operator associated to the cost function J = sum(m**2/f)' )

    def __call__(self, field, gamma):
        return field.proximalJ(gamma)

    def timing(self,nTiming,gamma=1.):
        t = 0.
        for i in xrange(nTiming):
            field = grid.CenteredField.random(self.N,self.P)
            time_start = tm.time()
            field = self(field,gamma)
            t += tm.time() - time_start
        return t
