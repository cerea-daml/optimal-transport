#########
# plot.py
#########

from mpl_toolkits.axes_grid1 import make_axes_locatable

def plottingOptions():
    options = ['b-', 'g-', 'r-', 'm-', 'y-', 'c-', 'k-',
               'b--','g--','r--','m--','y--','c--','k--',
               'b:', 'g:', 'r:', 'm:', 'y:', 'c:', 'k:',
               'b-.','g-.','r-.','m-.','y-.','c-.','k-.']
    n       = len(options)
    return (options, n)

def plottingOptionsMultiSim():

    options = [['b-', 'g-', 'r-', 'm-', 'y-', 'c-', 'k-'],
               ['b--','g--','r--','m--','y--','c--','k--'],
               ['b:', 'g:', 'r:', 'm:', 'y:', 'c:', 'k:' ],
               ['b-.','g-.','r-.','m-.','y-.','c-.','k-.']]

    n       = len(options[0])
    m       = len(options)
    return (options, m, n)

def plot(ax, Y, X=None, opt=None, **kwargs):
    args = []
    if X is not None:
        args.append(X)
    args.append(Y)
    if opt is not None:
        args.append(opt)

    return ax.plot(*tuple(args), **kwargs)

def tryAddCustomLegend(ax):
    divider = make_axes_locatable(ax)
    lax     = divider.append_axes('right', '10%',frameon=False)
    lax.set_yticks([])
    lax.set_xticks([])

    try:
        ax.legend(fontsize='xx-small', loc='center right', bbox_to_anchor=(1.13, 0.5), fancybox=True, framealpha=0.40)
    except:
        ax.legend(fontsize='xx-small', loc='center right', bbox_to_anchor=(1.13, 0.5), fancybox=True)
