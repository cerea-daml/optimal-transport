import numpy as np
import scipy.fftpack as fft

class ProxCdiv:
    '''
    Utils related to the divergence constrain
    C_div = { U in E_s \ div(U)=0 }
          = { U in E_s \ A_div.U = (0) }
    '''

    def __init__(self, M, N, P):
        self.M = M
        self.N = N
        self.P = P
        x = np.arange(M+1)
        y = np.arange(N+1)
        z = np.arange(P+1)

        Xm,Ym,Zm =np.meshgrid(x,y,z,indexing='ij')
        self.eigvalues_A_div = ( 2. * (M**2) * ( 1. - np.cos( np.pi * ( Xm + 1. ) / ( M + 2. ) ) ) +
                                 2. * (N**2) * ( 1. - np.cos( np.pi * ( Ym + 1. ) / ( N + 2. ) ) ) +
                                 2. * (P**2) * ( 1. - np.cos( np.pi * ( Zm + 1. ) / ( P + 2. ) ) ) )

    def __repr__(self):
        return ( 'Proximal operator associated to the divergence free constrain on a grid with shape' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : Prox_C_div')

    def A_div(self,grid):
        return grid.divergence()

    def T_A_div(self,div):
        return StaggeredGrid.T_divergence(div)

    def A_T_A_div(self,div):
        return self.A_div(self.T_A_div(div))

    def inv_A_T_A_div(self,div):
        # inverts operator A o T_A

        div = 0.5*fft.dst(div, type=1, axis=0)
        div = 0.5*fft.dst(div, type=1, axis=1)
        div = 0.5*fft.dst(div, type=1, axis=2)
        
        div = div/self.eigvalues_A_div

        div = fft.dst(div, type=1, axis=0) / ( self.M + 2. )
        div = fft.dst(div, type=1, axis=1) / ( self.N + 2. )
        div = fft.dst(div, type=1, axis=2) / ( self.P + 2. )
        return div
