#!/usr/bin/python3
"""
scoregui.py handle score.py3 configuration.
"""

import configparser
import glob
from tkinter import *
from tkinter import ttk
import os

config = configparser.ConfigParser()
config.read('score.ini')

# directory of problems to score
problemFiles = config['Paths']['ProblemFiles']
# directory of reference answers
answerFiles  = config['Paths']['AnswerFiles']
# filename of HTML output
HTML         = config['Paths']['HTMLOutput']
css          = config['Paths']['cssOutput']
Refresh      = config['HTML']['Refresh']
# Elegance bonus multipler
Elegance     = config.getint('Bonus','Elegance',fallback=1)
# Read in Bonus Points
BPList       = config['Bonus']['BP']
BonusPoints = [(x.split(',')[0].strip(),
                x.split(',')[1].strip(),
                int(x.split(',')[2])) for x in BPList.split(':')]

# extract the problem numbers BonusPoint, to be used to test for valid problems
problist = [pnum for pnum,pname,ppt in BonusPoints]

# find the elegance files
# the list entries will look like '01-JGH'
ele = [x.split('/')[-1].split('.')[0].upper() for x in glob.glob(problemFiles+'*.[eE][lL][eE]')]

# DefaultPoints is the list of possible problems, from 00 to 99.
DefaultPoints = [("{:0>2d}".format(q), '', 1) for q in range(0,100)]

# Team names
Teams = set(x.split('/')[-1].split('.')[0].split('-')[1].upper() for x in glob.glob(problemFiles+'*.*'))

def test(*args):
    ''' callback procedure for checkbox changes '''
    print (args, chkbtn[args[0]], intvar_dict[chkbtn[args[0]]].get())
    team_name = chkbtn[args[0]]
    team_state = intvar_dict[chkbtn[args[0]]].get()
    
    if team_state:
        print('enable')
        files = open(problemFiles+'00-'+team_name+'.ELE','a')
        files.close()
    else:
        print('disable')
        os.remove(problemFiles+'00-'+team_name+'.ELE')
        
    for key, value in intvar_dict.items():
        if value.get():
            print('selected:', key, value, value.get())

root = Tk()
root.title('Score Settings')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
ttk.Label(mainframe, text="Mark Teams",background='white').grid(column=0, row=0, sticky=(W, E))

# set up the checkbuttons and link to vars
intvar_dict = {}
j = 1
for t in Teams:
    j += 1
    # create the tk linked variable
    intvar_dict[t] = IntVar()
    # create the checkbox for team t and wire it to the tk linked variable
    c = ttk.Checkbutton(mainframe, text=t, variable=intvar_dict[t])
    # if there's an elegance file, set the checkbutton
    if '00-'+t in ele:
        intvar_dict[t].set(1)
    # Set the callback program when the variable changes
    intvar_dict[t].trace("w", test)
    # place the checkbutton on the grid
    c.grid(column=0, row=j, sticky=(W, E))

# chkbtn links teamnames to checkbutton variables
chkbtn = {}
for child in intvar_dict:
    chkbtn[str(intvar_dict[child])] = child

#intvar_dict['WESTVIEW'].set(1)

root.bind('<Return>', test)
root.mainloop()
