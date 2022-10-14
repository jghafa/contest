#!/usr/bin/python3
"""
contestfiles.py3 is a script to load USB drives with contest information.
It's called via a right-click in the file browser with no files are selected.

contestfiles.py3 performs the following tasks:

Copy Problem files and rules to the specified directory - files that match Pro*.*
Copy Input files to the specified directory  - files that match Input*.txt

contestfiles.py3 parameters
argv[0] is the program name, contestfiles.py3
argv[1] is the target directory to receive the files.

contestfiles.py3 uses the same ini as score.py3.
config['Paths']['DescFiles'] is the location of the Problem Desscription files.
config['Paths']['InputFiles'] is the location of the Problem Input files.
config['Paths']['HandoutDir'] the new dir name on the target USB drive

Under Linux, the right-click action requires nautilus-action to define it.
sudo apt-get install nautilus-action

The action file needed by contestfiles.py3 has been exported as an action*.xml file.
The action file makes Files only offer action to .txt files.

tk is needed for the dialog box
sudo apt-get install python3-tk
"""

import sys
import os
import tkinter.messagebox
import configparser
import glob
import shutil

# Hide the tk dialog window behind the messagebox
root = tkinter.Tk()
# Stop using root.withdraw(), but set geometry to handle dual screens
root.geometry('1x1+700-250')

config = configparser.ConfigParser()
config.read('score.ini')

# directory of problem descriptions and inputs
DescFiles = config['Paths']['DescFiles']
InputFiles = config['Paths']['InputFiles']
# the name of the new dir where the files will be copied
path = config['Paths']['HandoutDir']

targetdir = sys.argv[1]

if targetdir[-1] != '/':
    targetdir += '/'

if tkinter.messagebox.askokcancel("Copy Files?", 'Copy files to\n' + targetdir + path,
                    default = tkinter.messagebox.OK):
    os.makedirs(targetdir+path, exist_ok=True)
    for file in glob.glob(DescFiles + 'Pro*.*'):
        shutil.copy(file, targetdir + path)
    for file in glob.glob(InputFiles + 'Input*.[tT][xX][tT]'):
        shutil.copy(file, targetdir + path)
    for file in glob.glob(InputFiles + 'word*.[tT][xX][tT]'):
        shutil.copy(file, targetdir + path)
