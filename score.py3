#!/usr/bin/python3
"""
score.py3 scores a programming contest.
Features:
Grades team submittals by comparing them to a reference answer, using the diff utility.
Assigns points to an entry, based on matching the reference and the time stamp of the entry.
Stores the sucessful entries in an SQLite3 database.
Writes results to an HTML file that auto refreshes.

Parameters to score are stored in score.ini.
"""

import configparser
import os
import subprocess
from datetime import datetime
import sqlite3

config = configparser.ConfigParser()
config.read('score.ini')

# directory of problems to score
problemFiles = config['Paths']['ProblemFiles']
# directory of reference answers
answerFiles  = config['Paths']['AnswerFiles']
# filename of HTML output
HTML         = config['Paths']['HTMLOutput']
css          = config['Paths']['cssOutput']

# Get the list of Bonus Points per problem
# convert the scores into a list of integers
points = [int(i) if i.isdigit() else i for i in config['Bonus']['Points'].split(',')]
# put the problem names into a list
problems = config['Bonus']['Problems'].split(',')
# pair the problems and points into a tuple, use it later for initializing bonus db
BonusPoints = list(zip(problems, points))

#Define the database. The database is completely rebuilt every program run.
SQLconn = sqlite3.connect('score.sqlite')
SQL = SQLconn.cursor()

SQL.execute("""drop table if exists score""")
SQL.execute("""
        create table score (
            problem text,
            team    text,
            solved  text,
            score   integer);
          """)

SQL.execute("""drop table if exists bonus""")
SQL.execute("""
        create table bonus (
            problem text,
            bonus   integer);
          """)

SQL.execute("""
        CREATE INDEX IF NOT EXISTS scoreindex ON score(problem ASC, solved ASC);
          """)

SQL.executemany('insert into bonus values (?,?)', BonusPoints )

#setup is complete
SQLconn.commit()


# Read in all the problems
for file in os.listdir(problemFiles):
    if file.endswith('.txt'):
        # Split filename at the dash, get the problem number
        f = file.split('-')
        problem = f[0]
        team    = f[1].split('.')[0]
        #solved  = datetime.datetime.fromtimestamp(os.path.getmtime(problemFiles+file))
        solved  = os.path.getmtime(problemFiles+file)

        #print (
        #datetime.datetime.fromtimestamp(os.path.getmtime(problemFiles+file)),
        #os.path.getmtime(problemFiles+file)
        #)

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
            # 
            SQL.execute("""SELECT solved 
                           FROM score 
                           WHERE problem = ? and team = upper(?)""",
                    (problem, team ))
            data = SQL.fetchone()
            if data is None:
                #print (problem, team, solved)
                SQL.execute("INSERT into score values (?, upper(?), ?, 0)", 
                    (problem, team, solved))
            else:
                if str(solved) < data[0]:
                    # found a better time for this team and problem
                    SQL.execute("""update score 
                                  set solved = ? 
                                  WHERE problem = ? and team = upper(?)""",
                        (solved, problem, team))
            SQLconn.commit()

# Read the database and set the scores
last = ''
scorelist=[]
for row in SQL.execute("""SELECT  score.problem, score.team, score.solved, 
                                  bonus.bonus, score.score 
                          FROM score, bonus 
                          WHERE score.problem = bonus.problem 
                          ORDER by score.problem, score.solved"""):
    prob = row[0]
    if last != prob:
        bonus = 3
        last = prob
    else:
        if bonus > 1 :
            bonus -= 1
    # SQLite does not like two cursors active at one time.
    # So save the data in scorelist, and update when this loop ends
    # scorelist contains the bonus, the problem name, and the team name
    scorelist.append((bonus,row[0],row[1]))

#update the scores with the bonuses saved in scorelist
SQL.executemany("""UPDATE score 
                   SET score = ? 
                   WHERE problem = ? and team = upper(?)""", 
                 scorelist )

#print (HTML) #temp debugging - html file name
f = open(HTML, 'w')

# Initial HTML headers
f.write ('''<html>
              <head>
                <title>Contest Scores</title>
                <meta http-equiv="refresh" content="20">
                <link rel="stylesheet" href="''' + css + '''">
              </head>
              <body><div class="bottom">
        ''')
# Team score table
f.write ("""  <div class="col"><table><caption>Scores</caption>
              <tr><td>Team</td><td>Score</td><td>Solved</td></tr>
         """)

for row in SQL.execute("""SELECT  team, sum(score) as TeamScore,count(team) as Completed
                          FROM score
                          GROUP by team
                          ORDER by TeamScore desc"""):
    f.write('<tr><td>'                 +     row[0]  + 
            '</td><td align="center">' + str(row[1]) + 
            '</td><td align="center">' + str(row[2]) + 
            '</td></tr>')
#end the score table
f.write ("""</table></div>""")

# Problems solved table
f.write ("""  <div class="col"><table><caption>Problems Solved</caption>
              <tr><td>Problem</td><td>Solved Count</td></tr>
         """)

for row in SQL.execute("""SELECT problem, count(problem) as countprob 
                          FROM score
                          GROUP by problem
                          ORDER by problem"""):

    f.write('</td><td align="center">' +     row[0]  + 
            '</td><td align="center">' + str(row[1]) + 
            '</td></tr>')
#end the problems solved table
f.write ("""</table></div>""")

# Problems solved table
f.write ("""  <div class="col"><table><caption>All Problems Solved</caption>
              <tr><td>Problem</td><td>Team</td><td>Time</td><td>Score</td></tr>
         """)

for row in SQL.execute("""SELECT  problem, team, solved, score
                          FROM score
                          ORDER by solved asc"""):
    f.write('</td><td align="center">'+     row[0]  + 
            '</td><td>'               + str(row[1]) + 
            '</td><td align="center">'+ 
             datetime.fromtimestamp(float(row[2])).strftime('%Y-%m-%d %H:%M:%S') +
            '</td><td align="center">'+ str(row[3]) + 
            '</td></tr>')
#end the problems solved table
f.write ("""</table></div>""")


# end the html body
f.write ("""</div></body></html>""")

f.close()

#close SQLite3
SQLconn.commit()
SQLconn.close()
