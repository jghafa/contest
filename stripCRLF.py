#!/usr/bin/python3
'''
Clean the trailing CR LF
'''

import configparser
import glob

def CleanFile(fname,ext='.new.txt'):
    with open(fname, "r") as f:
        filelist = f.readlines()
    filen = fname[0:-4]
    with open(fname+ext,"w") as f:
        for x in range(len(filelist)):
            if x < len(filelist) -1 :
                f.write(filelist[x].rstrip() + '\n')
            else:
                f.write(filelist[x].rstrip())

config = configparser.ConfigParser()
config.read('score.ini')

inputFiles  = config['Paths']['InputFiles']


for files in glob.glob(inputFiles+'*.[tT][xX][tT]'):
    CleanFile(files)
