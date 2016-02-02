#!/usr/bin/env python

import sys
import numpy   as np
import cPickle as pck

from .OT1D.OTObjects1D.grid import grid

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
