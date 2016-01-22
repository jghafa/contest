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
# filename of HTML output
HTML         = config['Paths']['HTMLOutput']
# Get the list of Bonus Points
points = [int(i) if i.isdigit() else i for i in config['Bonus']['Points'].split(',')]
problems = config['Bonus']['Problems'].split(',')
# pair the problems and points into a tuple, use it later for bonus db
BonusPoints = list(zip(problems, points))

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

#setup is complete
conn.commit()


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
            # 
            c.execute("SELECT solved FROM score WHERE problem = ? and team = upper(?)",
                    (problem, team ))
            data = c.fetchone()
            if data is None:
                #print (problem, team, solved)
                c.execute("insert into score values (?, upper(?), ?, 0)", 
                    (problem, team, solved))
            else:
                if str(solved) < data[0]:
                    # found a better time for this team and problem
                    c.execute("""update score 
                                set solved = ? 
                                WHERE problem = ? and team = upper(?)""",
                        (solved, problem, team))
            conn.commit()

# Read the database and set the scores
last = ''
scorelist=[]
for row in c.execute("""SELECT  score.problem, score.team, score.solved, 
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
    #print (bonus, row)
    # this list will update the table in a couple lines
    scorelist.append((bonus,row[0],row[1]))

c.executemany("""UPDATE score 
                 SET score = ? 
                 WHERE problem = ? and team = upper(?)""", 
                 scorelist )

print (HTML)
f = open(HTML, 'w')

f.write ("""<html>
              <head>
                <title>Contest Scores</title>
                <meta http-equiv="refresh" content="20">
              </head>
              <body>
              <h2>Contest Scores</h2>
                <table>
                    <tr><td><b>Team</td><td>Score</td><td>Solved</td></b></tr>
         """)



for row in c.execute("""SELECT  team, sum(score) as TeamScore,count(team) as Completed
                        FROM score
                        GROUP by team
                        ORDER by TeamScore desc"""):
    f.write ('<tr><td>' + row[0] + '</td><td>' + 
                    str(row[1]) + '</td><td>' + 
                    str(row[2]) + '</td></tr>')

f.write ("""
            </tr>
            </table>
          </body>
        </html>
""")

f.close()

#close SQLite3
conn.commit()
conn.close()
