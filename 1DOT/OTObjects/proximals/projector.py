#################
# Class Projector
#################
#
# Default code for a projector on an affine space
#
# assuming data is in a vector space E,
# projects v in E on { w in E \ A.w = kernel in A(E) }
# where A is a linear operator
#
# Note that one must have kernel in Im(A)
#

import ..OTObject

class Projector( OTObject ):
    '''
    Default class for a projector on an affine space
    '''

    def __init__( self ,
                  N , P ,
                  kernel ):
        OTObject._init__( self ,
                          N , P )
        self.kernel = kernel

    def __repr__(self):
        return ( 'Projector on an affine space.' )

    def A(self, vector):
        return vector

    def TA(self, vector):
        return vector

    def ATA(self, vector):
        return self.A( self.TA( vector ) )

    def inverseATA(self, vector):
        return vector

    def __call__(self, vector):
        Avector  = self.A( vector )
        Avector -= self.kernel
        Avector  = self.invATA( Avector )
        Avector  = self.TA( Avector )
        return ( vector - vector )

    def test(self):
        # requires the random functions
