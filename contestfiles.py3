#!/usr/bin/python3
"""
"""

import sys
import os
import tkinter.messagebox

# Hide the tk dialog window
root = tkinter.Tk()
root.withdraw()

path = 'ContestFiles2016'
tkinter.messagebox.askokcancel("test", str(sys.argv))

targetdir = sys.argv[1]

if targetdir[-1] != '/':
    targetdir += '/'

message = ' Copy files to\n' + targetdir + path


if tkinter.messagebox.askokcancel("Copy Files?", message,
                    default = tkinter.messagebox.CANCEL):
    os.makedirs(targetdir+path, exist_ok=True)
    pass
