###############
# saveResult.py
###############

import cPickle as pck

from .files import fileResult

def saveResult(outputDir, result):
    f = open(fileResult(outputDir), 'wb')
    p = pck.Pickler(f, protocol=-1)
    p.dump(result)
    f.close()

