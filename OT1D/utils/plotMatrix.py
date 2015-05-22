###############
# plotMatrix.py
###############

def plotMatrix(ax, matrix, plotter='imshow', **kwargs):
    if plotter == 'imshow':
        return ax.imshow(matrix, **kwargs)
    elif plotter == 'contour':
        return ax.contour(matrix, **kwargs)
    elif plotter == 'contourf':
        return ax.contourf(matrix, **kwargs)
