#########
# cmap.py
#########

from matplotlib import cm

def colormap(cmapName):
    try:
        return cm.__getattribute__(cmapName)
    except:
        return cm.jet
