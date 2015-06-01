########
# run.py
########

import os
import sys

def runCommand(command, printIO):
    status = os.system(command)
    if printIO:
        print(command)
    if status != 0:
        sys.exit(status)
