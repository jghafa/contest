#!/usr/bin/python3
"""
trans.py3 is a script to quickly handle progamming submissions on game day.
It's meant to be called via a right-click in the file browser.

trans.py3 performs the following tasks:

Transfer files to the game directory
Creates a log of files processed
Calls the score program

trans.py3 parameters
argv[0] is the program name, trans.py3
argv[1] is the directory that contains the files to transfer.
argv[2] is the first file name to transfer.
argv[x] are the rest of the file names to transfer

trans.py3 uses the same ini as score.py3, as they both are concerned with the same files

Under Linux, the right-click action requires nautilus-action to define it.
sudo apt-get install nautilus-action

The action file needed by trans.py3 has been exported as an action*.xml file.
The action file makes Files only offer action to .txt files.

tk is needed for the dialog box
sudo apt-get install python3-tk
"""

import sys
import configparser
import subprocess
from datetime import datetime
import os
import tkinter.messagebox

# Hide the tk dialog window
root = tkinter.Tk()
root.withdraw()

config = configparser.ConfigParser()
config.read('score.ini')

# directory of problems to score
problemFiles = config['Paths']['ProblemFiles']
# location of the log file
logOutput=config['Paths']['logOutput']
# location of the score program file
scoreProg=config['Paths']['scoreProg']

log = open(logOutput, 'a')

# loop through the parameters to get the files to copy
for a in range(2, len(sys.argv)):
    #check if the file is already there, as the file date will get reset
    if os.path.isfile(problemFiles+sys.argv[a]):
        if tkinter.messagebox.askokcancel("Duplicate Entry.", 
                         "Click OK to submit again.\n"+sys.argv[a]):
            pass
        else:
            log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                'Canceled submit for ' + sys.argv[a]+ '\n')
            continue
    # OK, copy the file
    x = subprocess.check_call(['cp',
                                sys.argv[1] + '/' + sys.argv[a],
                                problemFiles])
    log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                sys.argv[1] + '/' + sys.argv[a]+ '\n')

# calc the scores and update the html
try:
    x = subprocess.check_call([scoreProg])
except FileNotFoundError as e:
    log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                'error - score not found' + '\n')

log.close()
