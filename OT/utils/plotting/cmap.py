#________
# cmap.py
#________

from matplotlib import cm

#__________________________________________________

def colormap(cmapName):
    try:
        return cm.__getattribute__(cmapName)
    except:
        return cm.jet

#__________________________________________________

