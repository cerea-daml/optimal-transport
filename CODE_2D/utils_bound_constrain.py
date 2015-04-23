import numpy as np
import time as tm

from utils_grid import *

class ProxCbound:
    '''
    Utils related to the boundary condition constrain
    C_b = { U in E_s \ boundary(U) = (m_left,m_right,m_down,m_up,f_init,f_final) }
    '''

    def __init__(self, M, N, P,
                 mx0=None, mx1=None,
                 my0=None, my1=None,
                 f0=None,  f1=None):
        self.M = M
        self.N = N
        self.P = P

        if mx0 is None:
            self.mx0 = np.zeros(shape=(N+1,P+1))
        else:
            self.mx0 = mx0

        if mx1 is None:
            self.mx1 = np.zeros(shape=(N+1,P+1))
        else:
            self.mx1 = mx1

        if my0 is None:
            self.my0 = np.zeros(shape=(M+1,P+1))
        else:
            self.my0 = my0

        if my1 is None:
            self.my1 = np.zeros(shape=(M+1,P+1))
        else:
            self.my1 = my1

        if f0 is None:
            self.f0 = np.zeros(shape=(M+1,N+1))
        else:
            self.f0 = f0

        if f1 is None:
            self.f1 = np.zeros(shape=(M+1,N+1))
        else:
            self.f1 = f1

    def __repr__(self):
        return ( 'Proximal operator associated to the boundary condition constrain on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCbound')

    def __call__(self, grid, overwrite=True):
        # projects StaggeredGrid grid on the boundary condition constrain space        
        if overwrite:
            grid.mx[0,:,:]        = self.mx0[:,:]
            grid.mx[self.M+1,:,:] = self.mx1[:,:]
            grid.my[:,0,:]        = self.my0[:,:]
            grid.my[:,self.N+1,:] = self.my1[:,:]
            grid.f[:,:,0]         = self.f0[:,:]
            grid.f[:,:,self.P+1]  = self.f1[:,:]
            return grid
        else:
            return self(grid.copy(), True)

    def timing(self,nTiming, overwrite=True):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid,overwrite)
            t += tm.time() - time_start
        return t

class ProxCtempbound:
    '''
    Utils related to the temporal boundary condition constrain
    C_tb = { U in E_s \ temporalBoundary(U) = (f_init,f_final) }
    '''

    def __init__(self, M, N, P,
                 f0=None, f1=None):
        self.M = M
        self.N = N
        self.P = P

        if f0 is None:
            self.f0 = np.zeros(shape=(M+1,N+1))
        else:
            self.f0 = f0

        if f1 is None:
            self.f1 = np.zeros(shape=(M+1,N+1))
        else:
            self.f1 = f1

    def __repr__(self):
        return ( 'Proximal operator associated to the temporal boundary condition constrain on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCtempbound')

    def __call__(self, grid, overwrite=True):
        # projects StaggeredGrid grid on the temporal boundary condition constrain space
        if overwrite:
            grid.f[:,:,0]         = self.f0[:,:]
            grid.f[:,:,self.P+1]  = self.f1[:,:]
            return grid
        else:
            return self(grid.copy(), True)

    def timing(self,nTiming, overwrite=True):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid,overwrite)
            t += tm.time() - time_start
        return t

class ProxCresbound:
    '''
    Utils related to the boundary condition constrain with a reservoir
    C_rb = { U in E_s \ boundary(U) = (m_left,m_right,m_down,m_up,f_init[1:M,1:N],f_final[1:M,1:N] & deltaMass(U) = deltaMass) }
    '''

    def __init__(self, M, N, P,
                 deltaMass=0.,
                 mx0=None, mx1=None,
                 my0=None, my1=None,
                 f0=None,  f1=None):
        self.M = M
        self.N = N
        self.P = P
        self.deltaMass = deltaMass

        if mx0 is None:
            self.mx0 = np.zeros(shape=(N+1,P+1))
        else:
            self.mx0 = mx0

        if mx1 is None:
            self.mx1 = np.zeros(shape=(N+1,P+1))
        else:
            self.mx1 = mx1

        if my0 is None:
            self.my0 = np.zeros(shape=(M+1,P+1))
        else:
            self.my0 = my0

        if my1 is None:
            self.my1 = np.zeros(shape=(M+1,P+1))
        else:
            self.my1 = my1

        if f0 is None:
            self.f0 = np.zeros(shape=(M+1,N+1))
        else:
            self.f0 = f0

        if f1 is None:
            self.f1 = np.zeros(shape=(M+1,N+1))
        else:
            self.f1 = f1


    def __repr__(self):
        return ( 'Proximal operator associated to the boundary condition constrain with a reservoir on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCresbound')

    def __call__(self, grid, overwrite=True):
        # projects StaggeredGrid grid on the boundary condition constrain space        
        if overwrite:
            grid.mx[0,:,:]        = self.mx0[:,:]
            grid.mx[self.M+1,:,:] = self.mx1[:,:]
            grid.my[:,0,:]        = self.my0[:,:]
            grid.my[:,self.N+1,:] = self.my1[:,:]

            grid.f[1:self.M,1:self.N,0]         = self.f0[1:self.M,1:self.N]
            grid.f[1:self.M,1:self.N,self.P+1]  = self.f1[1:self.M,1:self.N]

            deltaMassCurrent = ( grid.f[0,:,self.P+1].sum() + 
                                 grid.f[self.M,:,self.P+1].sum() +
                                 grid.f[1:self.M,0,self.P+1].sum() + 
                                 grid.f[1:self.M,self.N,self.P+1].sum() ) - self.deltaMass

            deltaMassCurrent /= 2. * self.M + 2. * self.N

            grid.f[0,:,self.P+1]             -= deltaMassCurrent
            grid.f[self.M,:,self.P+1]        -= deltaMassCurrent
            grid.f[1:self.M,0,self.P+1]      -= deltaMassCurrent
            grid.f[1:self.M,self.N,self.P+1] -= deltaMassCurrent

            grid.f[0,:,0]             = 0.
            grid.f[self.M,:,0]        = 0.
            grid.f[1:self.M,0,0]      = 0.
            grid.f[1:self.M,self.N,0] = 0.

            return grid
        else:
            return self(grid.copy(), True)

    def timing(self,nTiming, overwrite=True):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid,overwrite)
            t += tm.time() - time_start
        return t
