#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

######################
# extractFinalState.py
######################

import numpy   as np
import pickle as pck

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
