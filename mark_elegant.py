#!/usr/bin/python3
"""
mark_elegant.py is a script to give bonus points.
It's meant to be called via a right-click in the file browser.

mark_elegant.py performs the following tasks:

Read the input file
Copy to submit dir with .ele
Calls the score program

mark_elegant.py3 parameters
argv[0] is the program name, trans.py3
argv[1] is the directory that contains the files to transfer.
argv[2] is the first file name to transfer.
argv[x] are the rest of the file names to transfer

mark_elegant.py uses the same ini as score.py3.
config['Paths']['ProblemFiles'] - Where to put the files to be judged
config['Paths']['logOutput'] - the log file location
config['Paths']['scoreProg'] - the script to calc and show the score

Under Linux, the right-click action requires nautilus-action to define it.
sudo apt-get install nautilus-action

The action file needed by mark_elegant.py has been exported as an action*.xml file.
The action file makes Files only offer action to .txt files.

tk is needed for the dialog box
sudo apt-get install python3-tk
"""

import sys
import configparser
import shutil
from datetime import datetime
import os

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
    fname = os.path.basename(sys.argv[a])
    # Split filename at the dash, get the problem number
    f = fname.split('-')
    # if the filename has no problem number, continue to next file
    if len(f) < 2:
        continue
    problem = f[0]
    team    = f[1].split('.')[0]

    # OK, copy the file
    sourcedir = sys.argv[1]
    if sourcedir[-1] != '/':
        sourcedir += '/'
    log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 'elegant' +
                sourcedir + fname + '\n')
    shutil.copy(sourcedir + fname, problemFiles+problem+'-'+team+'.ELE')
 
# calc the scores and update the html
try:
    exec(open(scoreProg).read())
except FileNotFoundError as e:
    log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                'error - score not found' + '\n')

log.close()
