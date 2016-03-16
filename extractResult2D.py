#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#!/usr/bin/env python

import sys
import numpy   as np
import cPickle as pck

from OT.OTObjects2D.grid import grid

#__________________________________________________

fn = sys.argv[1]

f  = open(fn, 'rb')
p  = pck.Unpickler(f)
fS = p.load()
f.close()

fn = fn.replace('.bin', '.npy')
np.save(fn, fS.convergingStaggeredField().f)
print('Written '+fn+' ...')

#__________________________________________________
