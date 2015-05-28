##################
# saveAnimation.py
##################

from matplotlib.animation import AVConvWriter
from matplotlib.animation import FFMpegWriter
from matplotlib.animation import MencoderWriter

def makeMovieWriter(writerName='ffmpeg', writerFPS=5, writerCodec=None, writerBitrate=None, writerExtraArgs=None):
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
            anim.save(figName, writer=writer)
        except:
            print('Could not write '+figName+' ...')
