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
    return ( state.convergingStaggeredField() - finalState.convergingStaggeredField() ).LInftyNorm()


 

