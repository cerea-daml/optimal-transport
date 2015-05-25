#######################
# definePlotSubplots.py
#######################

def defaultPlotSubplots(iterOrTime = 'iterations', xScale='log', yScale='log', grid=True):
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

def customPlotSubplots(iterOrTime = 'iterations', xScale='log', yScale='log', grid=True):
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
