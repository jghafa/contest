#!/usr/bin/python3
"""
LoadRefFile.py3 is a script to run all the program files,
and load their output to the reference directory.
"""

from datetime import datetime
import configparser
import glob
import subprocess

config = configparser.ConfigParser()
config.read('score.ini')

# directory of problem descriptions and inputs
HomeDir = config['Paths']['DescFiles']
CodeFiles = config['Paths']['CodeFiles']
AnswerFiles = config['Paths']['AnswerFiles']
ProblemFiles = config['Paths']['ProblemFiles']

#targetdir = sys.argv[1]

#if targetdir[-1] != '/':
#    targetdir += '/'


for file in glob.glob(CodeFiles + '[0123456789][0123456789].py'):
    #shutil.copy(file, targetdir + path)
    ProgA = (file
            + ' > '
            + AnswerFiles
            + file.split('/')[-1].split('.')[0]
            + '.txt')
    ProgP = (file
            + ' > '
            + ProblemFiles
            + file.split('/')[-1].split('.')[0]
            + '-JGH.txt')
    print (file.split('/')[-1].split('.')[0],datetime.now().strftime('%m/%d %H:%M:%S'))
    x = subprocess.run([ProgA],
         cwd=CodeFiles,
         stdout=subprocess.DEVNULL,
         shell=True)
    x = subprocess.run([ProgP],
         cwd=CodeFiles,
         stdout=subprocess.DEVNULL,
         shell=True)

print('Done')
