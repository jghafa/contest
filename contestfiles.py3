#!/usr/bin/python3
"""
"""

import sys
import os
import tkinter.messagebox
import configparser
import glob
import shutil

# Hide the tk dialog window
root = tkinter.Tk()
root.withdraw()

config = configparser.ConfigParser()
config.read('score.ini')

# directory of problems to score
TeamHandouts = config['Paths']['TeamHandouts']
path = config['Paths']['HandoutDir']

targetdir = sys.argv[1]

if targetdir[-1] != '/':
    targetdir += '/'

if tkinter.messagebox.askokcancel("Copy Files?", 'Copy files to\n' + targetdir + path,
                    default = tkinter.messagebox.CANCEL):
    os.makedirs(targetdir+path, exist_ok=True)
    for file in glob.glob(TeamHandouts + 'Problem*.txt'):
        shutil.copy(file, targetdir + path)
    for file in glob.glob(TeamHandouts + 'Input*.txt'):
        shutil.copy(file, targetdir + path)
