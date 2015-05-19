###########
# cardan.py
###########
#
# Uses Cardan formula to find roots for degree 3 polynoms 
#

import numpy as np
import time

def reducePolynom(a,b,c,d):
    p = -1.*b*b/(3.*a*a) + 1.*c/a
    q = (1.*b/(27.*a))*(2.*b*b/(a*a)-9.*c/a) + 1.*d/a
    return p,q

def delta(p,q):
    return 4*p*p*p + 27*q*q

def solutionPQ(p,q):
    d       = delta(p,q)
    rac_d   = np.sqrt(abs(d))
    u       = 0.5*(-27.*q+3.*np.sqrt(3.)*rac_d)
    v       = 0.5*(-27.*q-3.*np.sqrt(3.)*rac_d)
    rac_3_u = -np.power(abs(u),1./3.)*(u<0) + np.power(np.abs(u),1./3.)*(u>=0)
    rac_3_v = -np.power(abs(v),1./3.)*(v<0) + np.power(np.abs(v),1./3.)*(v>=0)

    root0   = (rac_3_u+rac_3_v)/3.

    uc      = 0.5*(-27.*q+3.*np.sqrt(3.)*rac_d*1j)
    uc      = np.power(uc,1./3.)
    root1   = (uc+np.conj(uc))/3.
    root1   = root1.real
    
    uc      = uc *(np.exp(2.*np.pi*1j/3.))
    root2   = (uc+np.conj(uc))/3.
    root2   = root2.real

    uc      = uc *(np.exp(2.*np.pi*1j/3.))
    root3   = (uc + np.conj(uc))/3.
    root3   = root3.real

    return (root0*(d>0)+root1*(d<=0), root0*(d>0)+root2*(d<=0), root0*(d>0)+root3*(d<=0))

def solutionABCD(a,b,c,d):
    p,q      = reducePolynom(a,b,c,d)
    r0,r1,r2 = solutionPQ(p,q)
    shift    = -b/(3*a)
    return r0+shift,r1+shift,r2+shift

def maxRoot(a,b,c,d):
    r0,r1,r2 = solutionABCD(a,b,c,d)
    return np.maximum(np.maximum(r0,r1),r2)

#__________________________________________________
# Test routines

def maxRootNaiv(a,b,c,d):
    r = np.roots([a,b,c,d])
    r_real = r[np.isreal(r)]
    return np.max(r_real).real

def maxRootNaivVect(a,b,c,d,N):
    res = np.zeros(N)
    for i in xrange(N):
        res[i] = maxRootNaiv(a[i],b[i],c[i],d[i])
    return res

def testMaxRootVect(N):
    a  = np.random.rand(N) + 1e-3
    b  = np.random.rand(N) - 0.5
    c  = np.random.rand(N) - 0.5
    d  = np.random.rand(N) - 0.5
    t0 = time.time()
    r0 = maxRootNaivVect(a,b,c,d,N)
    t1 = time.time()
    r1 = maxRoot(a,b,c,d)
    t2 = time.time()
    e  = abs(r0 - r1).sum()
    print 'number of tests :', N
    print 'max error =', e
    print 'time non verctorized :', t1-t0
    print 'time vectoried :', t2-t1
    return e
