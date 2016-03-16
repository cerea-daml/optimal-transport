#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
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

from .. import OTObject as oto

class Projector( oto.OTObject ):
    '''
    Default class for a projector on an affine space
    '''

    def __init__( self ,
                  N , P ,
                  kernel ):
        oto.OTObject.__init__( self ,
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
        Avector  = self.inverseATA( Avector )
        Avector  = self.TA( Avector )
        return ( vector - Avector )

