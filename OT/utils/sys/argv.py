#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#########
# argv.py
#########

import sys

def extractArgv():
    sys.argv.pop(0)
    arguments = {}
    for arg in sys.argv:
        members               = arg.split('=')
        arguments[members[0]] = members[1]

    return arguments
