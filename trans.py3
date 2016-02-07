#!/usr/bin/python3
"""
Transfer files to the game directory, with a log of files moved

In Linux, you can invoke the program via a right-click in Files.
The right-click action requires nautilus-action to set it up.
sudo apt-get install nautilus-action

The action file needed by trans.py3 has been exported as an action*.xml file.
The action file has been limited to only send .txt files to trans.py3.

trans.py3 parameters
argv[0] is the program name, trans.py3
argv[1] is the directory that contains the files to transfer.
argv[2] is the first file name to transfer.
argv[x] are the rest of the file names to transfer

trans.py3 uses the same ini as score.py3, as they both are concerned with the same files
"""

import sys
import configparser
import subprocess
from datetime import datetime

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
