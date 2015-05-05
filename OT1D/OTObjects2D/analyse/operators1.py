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
    return state.convergingStaggeredField().divergence().LInftyNorm()

def absMin(state):
    return abs( state.convergingStaggeredField().f.min() )

def functionalJ(state):
    return ( state.functionalJ() / ( state.M * state.N * state.P ) )

def make_functionalJeps(eps):
    def funcJeps(state):
        centField = state.convergingStaggeredField().interpolation()
        return ( ( ( np.power( centField.mx , 2. ) + 
                     np.power( centField.my , 2. ) ) / 
                   ( np.maximum( centField.f , eps ) ) ).sum() / 
                 ( state.M * state.N * state.P ) ) 
    return funcJeps
 

