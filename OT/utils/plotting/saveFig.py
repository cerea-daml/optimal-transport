#___________
# saveFig.py
#___________

#__________________________________________________

def saveFig(plt, figName, extensionsList):
    for ext in extensionsList:
        try:
            print('Writing '+figName+ext+' ...')
            plt.savefig(figName+ext)
        except:
            print('Could not write file '+figName+ext+' ...')

#__________________________________________________
