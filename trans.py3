#!/usr/bin/python3
"""
Transfer files to the game day directory
"""

import sys


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


# end the html body
f.write ("""</div></body></html>""")

f.close()

