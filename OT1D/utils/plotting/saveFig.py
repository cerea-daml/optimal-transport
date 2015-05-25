############
# saveFig.py
############

def saveFig(plt, figName, extensionsList):
    for ext in extensionsList:
        print('Writing '+figName+ext+' ...')
        plt.savefig(figName+ext)
