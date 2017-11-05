#!/usr/bin/python3
"""
openmeld.py3 is a script to quickly quickly open a visual
diff program for game day.
It's meant to be called via a right-click in the file browser.

Parameters
argv[0] is the program name
argv[1] is the directory that contains the files to transfer.
argv[2] is the first file name to transfer.
argv[x] are the rest of the file names to transfer

openmeld.py3 uses the same ini as score.py3.
config['Paths']['ProblemFiles'] - Where to put the files to be judged
config['Paths']['logOutput'] - the log file location
config['Paths']['scoreProg'] - the script to calc and show the score


Under Linux, the right-click action requires nautilus-action to define it.
sudo apt-get install nautilus-action

The action file needed by openmeldrans.py3 has been exported 
as an action*.xml file.
"""

import sys
import configparser
import subprocess
import os

config = configparser.ConfigParser()
config.read('score.ini')

# directory of problems to score
answerFiles  = config['Paths']['AnswerFiles']

# loop through the parameters to get the files to copy
fname = os.path.basename(sys.argv[1])
# Split filename at the dash, get the problem number
f = fname.split('-')
problem = f[0]

# Check for correct output
try:
    x = subprocess.check_call(['meld',
                                sys.argv[1],
                                answerFiles+problem+'.txt'],
                                stdout=subprocess.DEVNULL)
except subprocess.CalledProcessError as e:
    pass
