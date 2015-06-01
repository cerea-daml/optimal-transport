#########
# argv.py
#########

import sys

def extractArgv():
    sys.argv.pop(0)
    arguments = {}
    for arg in sys.argv:
        members               = arg.split('=')
        arguments[members[0]] = members[1]

    return arguments
