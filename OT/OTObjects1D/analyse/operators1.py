#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
###############
# operators1.py
###############
#
# operators in StaggeredField -> R
# to be used to analyse the results of a simulation
#

import numpy as np

def listOfOperators1():
    l = []
    l.append( ( maxDiv , '$max(div(m_n,f_n))$' ) )
    l.append( ( absMin , '$abs(min(f_n))$' ) )
    l.append( ( functionalJ , '$J(m_n,f_n)$' ) )

    eps = [ 1.e-10 , 1.e-8 , 1.e-6 , 1.e-4 ]
    
    for e in eps:
        funcJeps = make_functionalJeps(e)
        l.append( ( funcJeps , '$J_{'+str(e)+'}(m_n,f_n)$' ) )
    return l

def maxDiv(state):
    return state.divergence().LInftyNorm()

def absMin(state):
    return abs( state.f.min() )

def functionalJ(state):
    return ( state.interpolation().functionalJ() / ( state.N * state.P ) )

def make_functionalJeps(eps):
    def funcJeps(state):
        centField = state.interpolation()
        return ( np.power( centField.m , 2. ) / np.maximum( centField.f , eps ) ).sum() / ( state.N * state.P ) 
    return funcJeps
 

