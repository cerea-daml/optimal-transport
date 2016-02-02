#______________________
# definePlotSubplots.py
#______________________

#__________________________________________________

def definePlotSubplots(function, iterOrTime, xScale, yScale, grid):
    if 'customPlotSubplots':
        return customPlotSubplots(iterOrTime, xScale, yScale, grid)
    elif 'defaultPlotSubplots':
        return defaultPlotSubplots(iterOrTime, xScale, yScale, grid)

#__________________________________________________

def defaultPlotSubplots(iterOrTime, xScale, yScale, grid):
    columnsList         = [[[0]], 
                           [[1]], 
                           [[2]], 
                           [[2,3,4,5,6]], 
                           [[7]]]
    xAxisList           = [[iterOrTime for e in c] for c in columnsList]
    xScaleList          = [[xScale for e in c] for c in columnsList]
    yScaleList          = [[yScale for e in c] for c in columnsList]

    xLabelList          = [[iterOrTime for e in c] for c in columnsList]
    yLabelList          = [['$div$'],
                           ['$abs(min(.))$'],
                           ['$J$'],
                           ['$J$'],
                           ['']]
    titleList           = [['Divergence constrain'],
                           ['Positivity constrain'],
                           ['Cost function'],
                           ['Cost function'],
                           ['Convergence']]
    gridList            = [[grid for e in c] for c in columnsList]
    fileNameSuffixList  = ['DivConstrain',
                           'PosConstrain',
                           'J',
                           'moreJ',
                           'Convergence']

    return zip(columnsList, xAxisList, xScaleList, yScaleList, xLabelList, yLabelList, titleList, gridList, fileNameSuffixList)

#__________________________________________________

def customPlotSubplots(iterOrTime, xScale, yScale, grid):
    columnsList         = [[[0],[1]],
                           [[2]],
                           [[2],[2,3,4,5,6]],
                           [[7]]]

    xAxisList           = [[iterOrTime for e in c] for c in columnsList]
    xScaleList          = [[xScale for e in c] for c in columnsList]
    yScaleList          = [[yScale for e in c] for c in columnsList]

    xLabelList          = [[iterOrTime for e in c] for c in columnsList]

    yLabelList          = [['$div$', '$abs(min(.))$'],
                           ['$J$'],
                           ['$J$', '$J$'],
                           ['']]
    
    titleList           = [['Divergence constrain', 'Positivity constrain'],
                           ['Cost function'],
                           ['Cost function', 'Cost function'],
                           ['Convergence']]

    gridList            = [[grid for e in c] for c in columnsList]
    fileNameSuffixList  = ['Constrains',
                           'J',
                           'moreJ',
                           'Convergence']

    return zip(columnsList, xAxisList, xScaleList, yScaleList, xLabelList, yLabelList, titleList, gridList, fileNameSuffixList)

#__________________________________________________

