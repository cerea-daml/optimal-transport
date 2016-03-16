#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#_______________________
# defaultTransparency.py
#_______________________

#__________________________________________________

def getTransparencyFunction(name):

    def defaultTransparency(t):
        return t

    #_________________________
    
    def fastVanishingTransparency(t):
        if t < 0.6:
            return 0.0
        else:
            return 1. + ( 1.0 / 0.4 ) * ( t - 1.0 )

    #_________________________
        
    def customTransparency(t):
        return min(max(t, 0.25), 0.8)

    #_________________________

    if name == 'fastVanishingTransparency':
        return fastVanishingTransparency
    elif name == 'customTransparency':
        return customTransparency
    else:
        return defaultTransparency

#__________________________________________________
