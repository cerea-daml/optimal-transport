######################################
# Defines some possible configurations
######################################

import numpy as np

def boundaryGaussian(M,N,P,
                     A0,alphaX0,aplhaY0,x0,y0,
                     A1,alphaX1,alphaY1,x1,y1,normType=0):
    #
    # f0(x) = A0exp(-alphaX0(x-x0)^2)exp(-alphaY0(y-y0)^2)
    # f1(x) = A1exp(-alphaX1(x-x1)^2)exp(-alphaY1(y-y0)^2) normalized
    #

    # Normalize parameters
    x0n = np.mod(x0,1.)*M
    x1n = np.mod(x1,1.)*M
    y0n = np.mod(y0,1.)*N
    y1n = np.mod(y1,1.)*N
    alphaX0n = alphaX0/(M*M)
    alphaX1n = alphaX1/(M*M)
    alphaY0n = alphaY0/(N*N)
    alphaY1n = alphaY1/(N*N)

    # Defines f0 and f1
    x   = np.arange(M+1)
    y   = np.arange(N+1)
    X,Y = np.meshgrid(x,y,indexing='ij')

    f0  = A0 * np.exp( -alphaX0n * np.power( X - x0n , 2 ) ) * np.exp( -alphaY0n * np.power( Y - y0n , 2 ) )
    f1  = A1 * np.exp( -alphaX1n * np.power( X - x1n , 2 ) ) * np.exp( -alphaY1n * np.power( Y - y1n , 2 ) )

    mx0 = np.zeros(shape=(N+1,P+1))
    mx1 = np.zeros(shape=(N+1,P+1))
    my0 = np.zeros(shape=(M+1,P+1))
    my1 = np.zeros(shape=(M+1,P+1))

    return Boundary(M,N,P,
                    mx0, mx1,
                    my0, my1,
                    f0,  f1).normalize(normType)

def boundaryGaussian2(M,N,P,
                      A00,A01,alphaX00,alphaX01,alphaY00,alphaY01,x00,x01,y00,y01,
                      A10,A11,alphaX10,alphaX11,alphaY10,alphaY11,x10,x11,y10,y11,normType=0):
    #
    # f0(x) = A00exp(-alphaX00(x-x00)^2)exp(-alphaY00(x-y00)^2) + A01exp(-alphaX01(x-x01)^2)exp(-alphaY01(x-y01)^2)
    # f1(x) = A10exp(-alphaX10(x-x10)^2)exp(-alphaY10(x-y10)^2) + A11exp(-alphaX11(x-x11)^2)exp(-alphaY11(x-y11)^2)
    #

    # Normalize parameters
    x00n = np.mod(x00,1.)*M
    x01n = np.mod(x01,1.)*M
    x10n = np.mod(x10,1.)*M
    x11n = np.mod(x11,1.)*M

    y00n = np.mod(y00,1.)*N
    y01n = np.mod(y01,1.)*N
    y10n = np.mod(y10,1.)*N
    y11n = np.mod(y11,1.)*N
        
    alphaX00n = alphaX00/(M*M)
    alphaX01n = alphaX01/(M*M)
    alphaX10n = alphaX10/(M*M)
    alphaX11n = alphaX11/(M*M)

    alphaY00n = alphaY00/(N*N)
    alphaY01n = alphaY01/(N*N)
    alphaY10n = alphaY10/(N*N)
    alphaY11n = alphaY11/(N*N)

    # Defines f0 and f1
    x   = np.arange(M+1)
    y   = np.arange(N+1)
    X,Y = np.meshgrid(x,y,indexing='ij')

    f0  = ( A00 * np.exp( -alphaX00n * np.power( X - x00n , 2 ) ) * np.exp( -alphaY00n * np.power( Y - y00n , 2 ) ) +
            A01 * np.exp( -alphaX01n * np.power( X - x01n , 2 ) ) * np.exp( -alphaY01n * np.power( Y - y01n , 2 ) ) )

    f1  = ( A10 * np.exp( -alphaX10n * np.power( X - x10n , 2 ) ) * np.exp( -alphaY10n * np.power( Y - y10n , 2 ) ) +
            A11 * np.exp( -alphaX11n * np.power( X - x11n , 2 ) ) * np.exp( -alphaY11n * np.power( Y - y11n , 2 ) ) )

    mx0 = np.zeros(shape=(N+1,P+1))
    mx1 = np.zeros(shape=(N+1,P+1))
    my0 = np.zeros(shape=(M+1,P+1))
    my1 = np.zeros(shape=(M+1,P+1))

    return Boundary(M,N,P,
                    mx0, mx1,
                    my0, my1,
                    f0,  f1).normalize(normType)

def boundaryGaussianSplit1(M,N,P,
                           A00,A01,alphaX00,alphaX01,x00,x01,alphaY00,alphaY01,y00,y01,
                           A1,alphaX1,x1,alphaY1,y1,normType=0):
    #
    # f0(x) = A00exp(-alphaX00(x-x00)^2)exp(-alphaY00(y-y00)^2) + A01exp(-alphaX01(x-x01)^2)exp(-alphaY01(y-y01)^2)
    # f1(x) = A1exp(-alphaX1(x-x1)^2)exp(-alphaY1(y-y1)^2) normalized
    #

    # Normalize parameters
    x1n = np.mod(x1,1.)*M
    x00n = np.mod(x00,1.)*M
    x01n = np.mod(x01,1.)*M
    alphaX1n = alphaX1/(M*M)
    alphaX00n = alphaX00/(M*M)
    alphaX01n = alphaX01/(M*M)

    y1n = np.mod(y1,1.)*N
    y00n = np.mod(y00,1.)*N
    y01n = np.mod(y01,1.)*N
    alphaY1n = alphaY1/(N*N)
    alphaY00n = alphaY00/(N*N)
    alphaY01n = alphaY01/(N*N)

    # Defines f0 and f1
    x   = np.arange(M+1)
    y   = np.arange(N+1)
    X,Y = np.meshgrid(x,y,indexing='ij')

    f0  = ( A00 * np.exp( -alphaX00n * np.power( X - x00n , 2 ) ) * np.exp( -alphaY00n * np.power( Y - y00n , 2 ) ) +
            A01 * np.exp( -alphaX01n * np.power( X - x01n , 2 ) ) * np.exp( -alphaY01n * np.power( Y - y01n , 2 ) ) )

    f1  = ( A1  * np.exp( -alphaX1n  * np.power( X - x1n  , 2 ) ) * np.exp( -alphaY1n  * np.power( Y - y1n  , 2 ) ) )

    mx0 = np.zeros(shape=(N+1,P+1))
    mx1 = np.zeros(shape=(N+1,P+1))
    my0 = np.zeros(shape=(M+1,P+1))
    my1 = np.zeros(shape=(M+1,P+1))

    return Boundary(M,N,P,
                    mx0, mx1,
                    my0, my1,
                    f0,  f1).normalize(normType)

def boundaryGaussianSplit2(M,N,P,
                           A0,alphaX0,x0,alphaY0,y0,
                           A10,A11,alphaX10,alphaX11,x10,x11,alphaY10,alphaY11,y10,y11,normType=0):
    #
    # f0(x) = A0exp(-alphaX0(x-x0)^2)exp(-alphaY0(y-y0)^2) 
    # f1(x) = A10exp(-alphaX10(x-x10)^2)exp(-alphaY10(y-y10)^2) + A11exp(-alphaX11(x-x11)^2)exp(-alphaY11(y-y11)^2) normalized
    #

    # Normalize parameters
    x0n = np.mod(x0,1.)*M
    x10n = np.mod(x10,1.)*M
    x11n = np.mod(x11,1.)*M
    alphaX0n = alphaX0/(M*M)
    alphaX10n = alphaX10/(M*M)
    alphaX11n = alphaX11/(M*M)

    y0n = np.mod(y0,1.)*N
    y10n = np.mod(y10,1.)*N
    y11n = np.mod(y11,1.)*N
    alphaY0n = alphaY0/(N*N)
    alphaY10n = alphaY10/(N*N)
    alphaY11n = alphaY11/(N*N)

    # Defines f0 and f1
    x   = np.arange(M+1)
    y   = np.arange(N+1)
    X,Y = np.meshgrid(x,y,indexing='ij')

    f0  = ( A0  * np.exp( -alphaX0n  * np.power( X - x0n  , 2 ) ) * np.exp( -alphaY0n  * np.power( Y - y0n  , 2 ) ) )
    f1  = ( A10 * np.exp( -alphaX10n * np.power( X - x10n , 2 ) ) * np.exp( -alphaY10n * np.power( Y - y10n , 2 ) ) +
            A11 * np.exp( -alphaX11n * np.power( X - x11n , 2 ) ) * np.exp( -alphaY11n * np.power( Y - y11n , 2 ) ) )

    mx0 = np.zeros(shape=(N+1,P+1))
    mx1 = np.zeros(shape=(N+1,P+1))
    my0 = np.zeros(shape=(M+1,P+1))
    my1 = np.zeros(shape=(M+1,P+1))

    return Boundary(M,N,P,
                    mx0, mx1,
                    my0, my1,
                    f0,  f1).normalize(normType)

def boundaryGaussianSine(M,N,P,
                         A0,alphaX0,betaX0,alphaY0,betaY0,x00,x01,y00,y01,
                         A1,alphaX1,betaX1,alphaY1,betaY1,x10,x11,y10,y11,norm_type=0):
    #
    # f0 = A0exp(-alphaX0(x-x00)^2)exp(-alphaY0(y-y00)^2)sin^2(betaX0(x-x01))sin^2(betaY0(y-y01))
    # f1 = A1exp(-alphaX1(x-x10)^2)exp(-alphaY1(y-y10)^2)sin^2(betaX1(x-x11))sin^2(betaY1(y-y11)) normalized
    #

    # Normalize parameters
    x00n = np.mod(x00,1.)*M
    x01n = np.mod(x01,1.)*M
    x10n = np.mod(x10,1.)*M
    x11n = np.mod(x11,1.)*M

    y00n = np.mod(y00,1.)*N
    y01n = np.mod(y01,1.)*N
    y10n = np.mod(y10,1.)*N
    y11n = np.mod(y11,1.)*N

    alphaX0n = alphaX0/(M*M)
    alphaX1n = alphaX1/(M*M)
    betaX0n = betaX0/M
    betaX1n = betaX1/M

    alphaY0n = alphaY0/(N*N)
    alphaY1n = alphaY1/(N*N)
    betaY0n = betaY0/N
    betaY1n = betaY1/N

    # Defines f0 and f1
    x   = np.arange(M+1)
    y   = np.arange(N+1)
    X,Y = np.meshgrid(x,y,indexing='ij')

    f0  = ( A0 * np.exp( -alphaX0n * np.power( X - x00n , 2 ) ) * np.exp( -alphaY0n * np.power( Y - y00n , 2 ) ) *
            np.power( np.sin( betaX0n * ( X - x01n ) ) , 2 ) * np.power( np.sin( betaY0n * ( Y - y01n ) ) , 2 ) )
    f1  = ( A1 * np.exp( -alphaX1n * np.power( X - x10n , 2 ) ) * np.exp( -alphaY1n * np.power( Y - y10n , 2 ) ) *
            np.power( np.sin( betaX1n * ( X - x11n ) ) , 2 ) * np.power( np.sin( betaY1n * ( Y - y11n ) ) , 2 ) )

    mx0 = np.zeros(shape=(N+1,P+1))
    mx1 = np.zeros(shape=(N+1,P+1))
    my0 = np.zeros(shape=(M+1,P+1))
    my1 = np.zeros(shape=(M+1,P+1))

    return Boundary(M,N,P,
                    mx0, mx1,
                    my0, my1,
                    f0,  f1).normalize(normType)

def boundaryGaussianCosine(M,N,P,
                           A0,alphaX0,betaX0,alphaY0,betaY0,x00,x01,y00,y01,
                           A1,alphaX1,betaX1,alphaY1,betaY1,x10,x11,y10,y11,normType=0):
    #
    # f0 = A0exp(-alphaX0(x-x00)^2)exp(-alphaY0(y-y00)^2)cos^2(betaX0(x-x01))cos^2(betaY0(y-y01))
    # f1 = A1exp(-alphaX1(x-x10)^2)exp(-alphaY1(y-y10)^2)cos^2(betaX1(x-x11))cos^2(betaY1(y-y11)) normalized
    #

    # Normalize parameters
    x00n = np.mod(x00,1.)*M
    x01n = np.mod(x01,1.)*M
    x10n = np.mod(x10,1.)*M
    x11n = np.mod(x11,1.)*M

    y00n = np.mod(y00,1.)*N
    y01n = np.mod(y01,1.)*N
    y10n = np.mod(y10,1.)*N
    y11n = np.mod(y11,1.)*N

    alphaX0n = alphaX0/(M*M)
    alphaX1n = alphaX1/(M*M)
    betaX0n = betaX0/M
    betaX1n = betaX1/M

    alphaY0n = alphaY0/(N*N)
    alphaY1n = alphaY1/(N*N)
    betaY0n = betaY0/N
    betaY1n = betaY1/N

    # Defines f0 and f1
    x   = np.arange(M+1)
    y   = np.arange(N+1)
    X,Y = np.meshgrid(x,y,indexing='ij')

    f0  = ( A0 * np.exp( -alphaX0n * np.power( X - x00n , 2 ) ) * np.exp( -alphaY0n * np.power( Y - y00n , 2 ) ) *
            np.power( np.cos( betaX0n * ( X - x01n ) ) , 2 ) * np.power( np.cos( betaY0n * ( Y - y01n ) ) , 2 ) )
    f1  = ( A1 * np.exp( -alphaX1n * np.power( X - x10n , 2 ) ) * np.exp( -alphaY1n * np.power( Y - y10n , 2 ) ) *
            np.power( np.cos( betaX1n * ( X - x11n ) ) , 2 ) * np.power( np.cos( betaY1n * ( Y - y11n ) ) , 2 ) )

    mx0 = np.zeros(shape=(N+1,P+1))
    mx1 = np.zeros(shape=(N+1,P+1))
    my0 = np.zeros(shape=(M+1,P+1))
    my1 = np.zeros(shape=(M+1,P+1))

    return Boundary(M,N,P,
                    mx0, mx1,
                    my0, my1,
                    f0,  f1).normalize(normType)

def defaultBoundary(M, N, P, boundaryType, normType):
    if boundaryType == 0:
        # Gaussian

        A0 = 1.
        alphaX0 = M*M*0.05
        alphaY0 = N*N*0.05
        x0 = 0.375
        y0 = 0.375
        
        A1 = 1.
        alphaX1 = M*M*0.05
        alphaY1 = N*N*0.05
        x1 = 0.625
        y1 = 0.625

        return boundaryGaussian(M,N,P,
                                A0,alphaX0,alphaY0,x0,y0,A1,alphaX1,alphaY1,x1,y1,normType)

    elif boundaryType == 1:
        # Gaussian2
        A00 = 1.
        A01 = 1.
        alphaX00 = M*M*0.25
        alphaY00 = N*N*0.25
        alphaX01 = M*M*0.25
        alphaY01 = N*N*0.25
        x00 = 0.25
        x01 = 0.5
        y00 = 0.25
        y01 = 0.5
    
        A10 = 1.
        A11 = 1.
        alphaX10 = M*M*0.25
        alphaY10 = N*N*0.25
        alphaX11 = M*M*0.25
        alphaY11 = N*N*0.25
        x10 = 0.5
        y10 = 0.5
        x11 = 0.75
        y11 = 0.75
    
        return boundaryGaussian2(M,N,P,
                                 A00,A01,alphaX00,alphaX01,alphaY00,alphaY01,x00,x01,y00,y01,
                                 A10,A11,alphaX10,alphaX11,alphaY10,alphaY11,x10,x11,y10,y11,normType)

    elif boundaryType == 2:
        # GaussianSplit2
        A0 = 1.
        alphaX0 = M*M*0.05
        x0 = 0.5
        alphaY0 = N*N*0.05
        y0 = 0.5

        A10 = 1.
        A11 = 1.
        alphaX10 = M*M*0.1
        alphaX11 = M*M*0.1
        x10 = 0.25
        x11 = 0.75
        alphaY10 = N*N*0.1
        alphaY11 = N*N*0.1
        y10 = 0.25
        y11 = 0.75
        
        return boundaryGaussianSplit2(M,N,P,
                                      A0,alphaX0,x0,alphaY0,y0,
                                      A10,A11,alphaX10,alphaX11,x10,x11,alphaY10,alphaY11,y10,y11,normType)

    elif boundaryType == 3:
        # GaussianSplit1
        A00 = 1.
        A01 = 1.
        alphaX00 = M*M*0.1
        alphaX01 = M*M*0.1
        x00 = 0.25
        x01 = 0.75
        alphaY00 = N*N*0.1
        alphaY01 = N*N*0.1
        y00 = 0.25
        y01 = 0.75
        
        A1 = 1.
        alphaX1 = M*M*0.05
        x1 = 0.5
        alphaY1 = N*N*0.05
        y1 = 0.5

        return boundaryGaussianSplit1(M,N,P,
                                      A00,A01,alphaX00,alphaX01,x00,x01,alphaY00,alphaY01,y00,y01,
                                      A1,alphaX1,x1,alphaY1,y1,normType)

    elif boundaryType == 4:
        # GaussianSine
        A0 = 1.
        alphaX0 = M*M*0.05
        betaX0 = 16*np.pi
        alphaY0 = N*N*0.05
        betaY0 = 16*np.pi
        x00 = 0.25
        x01 = 0.
        y00 = 0.25
        y01 = 0.
        
        A1 = 1.
        alphaX1 = M*M*0.05
        betaX1 = 16*np.pi
        alphaY1 = N*N*0.05
        betaY1 = 16*np.pi
        x10 = 0.75
        x11 = 0.
        y10 = 0.75
        y11 = 0.

        return boundaryGaussianSine(M,N,P,
                                    A0,alphaX0,betaX0,alphaY0,betaY0,x00,x01,y00,y01,
                                    A1,alphaX1,betaX1,alphaY1,betaY1,x10,x11,y10,y11,normType)

    elif boundaryType == 5:
        A0 = 1.
        alphaX0 = M*M*0.05
        betaX0 = 16*np.pi
        alphaY0 = N*N*0.05
        betaY0 = 16*np.pi
        x00 = 0.25
        x01 = 0.
        y00 = 0.25
        y01 = 0.
        
        A1 = 1.
        alphaX1 = M*M*0.05
        betaX1 = 16*np.pi
        alphaY1 = N*N*0.05
        betaY1 = 16*np.pi
        x10 = 0.75
        x11 = 0.
        y10 = 0.75
        y11 = 0.

        return boundaryGaussianCosine(M,N,P,A0,alphaX0,betaX0,alphaY0,betaY0,x00,x01,y00,y01,
                                      A1,alphaX1,betaX1,alphaY1,betaY1,x10,x11,y10,y11,normType)
