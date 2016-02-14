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

trans.py3 uses the same ini as score.py3.
config['Paths']['ProblemFiles'] - Where to put the files to be judged
config['Paths']['logOutput'] - the log file location
config['Paths']['scoreProg'] - the script to calc and show the score


Under Linux, the right-click action requires nautilus-action to define it.
sudo apt-get install nautilus-action

The action file needed by trans.py3 has been exported as an action*.xml file.
The action file makes Files only offer action to .txt files.

tk is needed for the dialog box
sudo apt-get install python3-tk
"""

import sys
import configparser
import shutil
from datetime import datetime
import os
import tkinter.messagebox
import sqlite3

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

SQLfilename, file_extension = os.path.splitext(scoreProg)

SQLavailable = False
if os.path.isfile(SQLfilename+'.sqlite'):
    #SQL exists
    SQLconn = sqlite3.connect(SQLfilename+'.sqlite')
    SQL = SQLconn.cursor()
    SQLavailable = True
else:
    log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                ' SQLite file not found.\n')

# loop through the parameters to get the files to copy
for a in range(2, len(sys.argv)):
    fname = os.path.basename(sys.argv[a])
    if SQLavailable:
        # Split filename at the dash, get the problem number
        f = fname.split('-')
        # if the filename has no problem number, continue to next file
        if len(f) < 2:
            continue
        problem = f[0]
        team    = f[1].split('.')[0]
        # Did this team already solve the problem?
        SQL.execute("""SELECT solved 
                       FROM score 
                       WHERE problem = ? and team = upper(?)""",
                    (problem, team ))
        data = SQL.fetchone()
        if data is not None:
            # This team has already solved this one
            if tkinter.messagebox.askokcancel("Already Solved", 
                    "Click OK to submit again.\n"+fname,
                    default = tkinter.messagebox.CANCEL):
                log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                    'Already Solved ' + fname+ '\n')
                # Update anyway - this will change submit time to now.
                pass
            else:
                log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                    'Canceled submit for ' + fname+ '\n')
                #Don't submit again
                continue

    # OK, copy the file
    sourcedir = sys.argv[1]
    if sourcedir[-1] != '/':
        sourcedir += '/'
    log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                sourcedir + fname + '\n')
    shutil.copy(sourcedir + fname, problemFiles)
 
# calc the scores and update the html
try:
    exec(open(scoreProg).read())
except FileNotFoundError as e:
    log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                'error - score not found' + '\n')

log.close()
