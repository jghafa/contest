#!/usr/bin/python3
"""
Transfer files to the game directory via right-click in Files.

Require Linux and nautilus-action
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
logOutput=config['Paths']['logOutput']

log = open(logOutput, 'a')

f = open('test.HTML', 'w')

# Initial HTML headers
f.write ('''<html>
              <head>
                <title>test</title>
                <meta http-equiv="refresh" content="15">
              </head>
              <body><div class="body">
        ''')
f.write (str(sys.argv))
f.write ("""<br>""")
f.write (' to  dir = ' + problemFiles)
f.write ("""<br>""")
f.write ('from dir = ' + sys.argv[1])

#for a in sys.argv:
for a in range(2, len(sys.argv)):
    f.write ("""<br>""")
    f.write (str(a) +' = '+ sys.argv[a])
    x = subprocess.check_call(['cp',
                                sys.argv[1] + '/' + sys.argv[a],
                                problemFiles])
    log.write(datetime.now().strftime('%y/%m/%d %H:%M:%S, ') + 
                sys.argv[1] + '/' + sys.argv[a]+ '\n')

# end the html body
f.write ("""</div></body></html>""")

f.close()

