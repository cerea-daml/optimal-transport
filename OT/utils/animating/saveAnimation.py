#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
##################
# saveAnimation.py
##################

from matplotlib.animation import AVConvWriter
from matplotlib.animation import FFMpegWriter
from matplotlib.animation import MencoderWriter

def makeMovieWriter(writerName, writerFPS, writerCodec, writerBitrate, writerExtraArgs):
    if writerName == 'avconv':
        return AVConvWriter(fps=writerFPS, codec=writerCodec, bitrate=writerBitrate, extra_args=writerExtraArgs, metadata=None)
    elif writerName == 'ffmpeg':
        return FFMpegWriter(fps=writerFPS, codec=writerCodec, bitrate=writerBitrate, extra_args=writerExtraArgs, metadata=None)
    elif writerName == 'mencoder':
        return MencoderWriter(fps=writerFPS, codec=writerCodec, bitrate=writerBitrate, extra_args=writerExtraArgs, metadata=None)
    return

def saveAnimation(anim, figDir, prefixFigName, extensionsList, writer):
    for extension in extensionsList:
        figName = figDir + prefixFigName + extension
        print('Saving '+figName+' ...')
        try:
            anim.save(figName, writer=writer, dpi=100)
        except:
            print('Could not write '+figName+' ...')
