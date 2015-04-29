#####################
# defineBoundaries.py
#####################
#
# Function boundariesForConfig returns boundary conditions for the given configuration
#   config must define :
#     * N
#     * P
#     * dynamics
#     * boundaryType
#     * normType
#     * EPSILON
#
# Function boundariesFromFile returns boundary conditions from files
#

from ..grid import grid

from gaussian import defaultBoundaryGaussian
from gaussian import defaultBoundaryGaussian2
from gaussianSplit import defaultBoundaryGaussianSplit1
from gaussianSplit import defaultBoundaryGaussianSplit2
from gaussianSine import defaultBoundaryGaussianSine
from gaussianSine import defaultBoundaryGaussianCosine

def boundariesForConfig(config):
    # default configurations
    if config.boundaryType == 1:
        config.boundaries = defaultBoundaryGaussian( config.N , config.P )
    elif config.boundaryType == 2:
        config.boundaries = defaultBoundaryGaussian2( config.N , config.P )
    elif config.boundaryType == 3:
        config.boundaries = defaultBoundaryGaussianSplit1( config.N , config.P )
    elif config.boundaryType == 4:
        config.boundaries = defaultBoundaryGaussianSplit2( config.N , config.P )
    elif config.boundaryType == 5:
        config.boundaries = defaultBoundaryGaussianSine( config.N , config.P )
    elif config.boundaryType == 6:
        config.boundaries = defaultBoundaryGaussianCosine( config.N , config.P )

    # from file
    elif config.boundaryType == 0:
        files = [ config.filef0 , config.filef1 ]
        if config.dynamics == 0:
            files.append( config.filem0 )
            files.append( config.filem1 )
        boundaries = boundariesFromFile(files)
        config.boundaries = boundaries
        config.N = config.boundaries.N
        config.P = config.boundaries.P

    # normalize boundaries
    config.boundaries.normalize(config.normType)

    # adapt boundaries to dynamics
    if config.dynamics == 0:
        delta = config.boundaries.massDefault()
        if delta > config.EPSILON:
            print ('Changing dynamics because mass default is not compatible with dynamics=0.')

            if config.algoName == 'pd':
                config.dynamics = 1
            else:
                N = config.N
                bt0 = np.zeros(N+1+2)
                bt1 = np.zeros(N+1+2)
                bt0[1:N+2] = config.boundaries.temporalBoundaries.bt0[:]
                bt1[1:N+2] = config.boundaries.temporalBoundaries.bt1[:]
                temporalBoundaries = TemporalBoundaries( N+2, config.P, bt0, bt1 )
                spatialBoundaries  = config.boundaries.spatialBoundaries.copy()
                spatialBoundaries.N = N+2

                config.boundaries = Boundaries( N+2 , config.P , temporalBoundaries , spatialBoundaries )
                config.N = N+2
                
                if config.algoName == 'adr':
                    config.dynamics = 2
                elif config.algoName == 'adr3':
                    config.dynamics = 3

    if config.dynamics == 1:
        config.boundaries.spatialBoundaries = grid.SpatialBoundaries( config.N , config.P )
    elif config.dynamics == 2 or config.dynamics == 3:
        config.boundaries.spatialBoundaries = grid.SpatialBoundaries( config.N , config.P )
        config.boundaries.placeReservoir()

def extensionOfFile(fileName):
    if not '.' in fileName:
        return None
    else:
        l = fileName.split('.')
        return l[len(l)-1]

def arrayFromFile(fileName):
    if fileName is None or fileName == '':
        return None
    else:
        ext = extensionOfFile(fileName)

        if ext == 'npy':
            return np.load(fileName)
        else:
            return np.fromfile(fileName)

def boundariesFromFile(fileNames):
    while( len(fileNames) < 4 ):
        fileNames.append(None)

    bt0 = arrayFromFile( fileNames[0] )
    bt1 = arrayFromFile( fileNames[1] )
    bx0 = arrayFromFile( fileNames[2] )
    bx1 = arrayFromFile( fileNames[3] )

    if bt0 is None:
        bt0 = np.zeros(2)
    if bt1 is None:
        bt1 = np.zeros(2)
    if bx0 is None:
        bx0 = np.zeros(2)
    if bx1 is None:
        bx1 = np.zeros(2)

    N = max( bt0.size , bt1.size ) - 1
    P = max( bx0.size , bx1.size ) - 1

    f0 = np.zeros(N+1)
    f1 = np.zeros(N+1)
    m0 = np.zeros(P+1)
    m1 = np.zeros(P+1)
    
    f0[0:bt0.size] = bt0[:]
    f1[0:bt1.size] = bt1[:]
    m0[0:bx0.size] = bx0[:]
    m1[0:bx1.size] = bx1[:]

    temporalBoundaries = grid.TemporalBoundaries( N , P ,
                                                  f0 , f1 )
    spatialBoundaries = grid.SpatialBoundaries( N , P ,
                                                m0 , m1 )
    boundaries = grid.Boundaries( N , P ,
                                  temporalBoundaries, spatialBoundaries )

    return boundaries
