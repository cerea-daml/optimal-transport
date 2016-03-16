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
# operators2.py
###############
#
# operators in StaggeredField x StaggeredField -> R
# to be used to analyse the results of a simulation
#

def listOfOperators2():
    l = []
    l.append( ( convergence , '$|(m_n,f_n)-(m_\infty,f_\infty)|_{L^\infty}$' ) )
    return l

def convergence(state, finalState):
    return ( state - finalState ).LInftyNorm()


 

