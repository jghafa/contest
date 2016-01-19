#!/usr/bin/python3

import configparser
import os
import subprocess
import datetime
import sqlite3

config = configparser.ConfigParser()
config.read('score.ini')

# directory of problems to score
problemFiles = config['Paths']['ProblemFiles']
# directory of reference answers
answerFiles  = config['Paths']['AnswerFiles']
# Get the list of Bonus Points
points = [int(i) if i.isdigit() else i for i in config['Bonus']['Points'].split(',')]
problems = config['Bonus']['Problems'].split(',')
BonusPoints = list(zip(problems, points))

print (BonusPoints)

conn = sqlite3.connect('score.sqlite')
c = conn.cursor()

c.execute("""drop table if exists score""")
c.execute("""
        create table score (
            problem text,
            team    text,
            solved  text,
            score   integer);
          """)

c.execute("""drop table if exists bonus""")
c.execute("""
        create table bonus (
            problem text,
            bonus   integer);
          """)

c.execute("""
        CREATE INDEX IF NOT EXISTS scoreindex ON score(problem ASC, solved ASC);
          """)

c.executemany('insert into bonus values (?,?)', BonusPoints )

conn.commit()

quit()


# Read in all the problems
for file in os.listdir(problemFiles):
    if file.endswith('.txt'):
        # Split filename at the dash, get the problem number
        f = file.split('-')
        problem = f[0]
        team    = f[1].split('.')[0]
        solved  = datetime.datetime.fromtimestamp(os.path.getmtime(problemFiles+file))

        returncode = 0
        # Check for correct output
        try:
            x = subprocess.check_call(['diff','-w',
                                        problemFiles+file,
                                        answerFiles+problem+'.txt'],
                                        stdout=subprocess.DEVNULL)
        # diff succeeds when the answer is right, exceptions are wrong answers
        except subprocess.CalledProcessError as e:
            returncode = e.returncode

        # Return code of zero means the answer is correct
        if returncode == 0:
            c.execute("SELECT * FROM score WHERE problem = ? and team = upper(?)",
                    (problem, team ))
            data = c.fetchone()
            if data is None:
                print (problem, team, solved)
                c.execute("insert into score values (?, upper(?), ?, 1)", 
                    (problem, team, solved))
                conn.commit()

#close SQLite3
conn.commit()
conn.close()
