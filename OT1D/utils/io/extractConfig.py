######################
# extractFinalState.py
######################

import numpy   as np
import cPickle as pck

from .files import fileConfig

def extractConfig(outputDir):
    f              = open(fileConfig(outputDir),'rb')
    p              = pck.Unpickler(f)
    try:
        while True:
            config = p.load()
    except:
        f.close()

    return config
