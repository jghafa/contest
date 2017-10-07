#!/usr/bin/python3
"""
score.py3 scores a programming contest.
Features:
Grades team submittals by comparing them to a reference answer, using the diff utility.
Assigns points to an entry, based on matching the reference and the time stamp of the entry.
Stores the successful entries in an SQLite3 database.
Writes results to an HTML file that auto refreshes.

Parameters to score are stored in score.ini.
"""

import configparser
import os
import hashlib
import glob
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
Refresh      = config['HTML']['Refresh']

# Get the list of Bonus Points per problem
# convert the scores into a list of integers
#points = [int(i) if i.isdigit() else i for i in config['Bonus']['Points'].split(',')]
# put the problem numbers into a list
#problems = config['Bonus']['Problems'].split(',')
# put the problem names into a list
#probname = config['Bonus']['ProbName'].split(',')
# pair the problems, name and points into a tuple, 
# use it later for initializing bonus db
#BonusPoints = list(zip(problems, probname, points))

# New way inputing Bonus Points
BPList = config['Bonus']['BP']
BonusPoints = [(x.split(',')[0].strip(),
                x.split(',')[1].strip(),
                int(x.split(',')[2])) for x in BPList.split(':')]

# DefaultPoints is the list of possible problems, from 00 to 99.
DefaultPoints = [("{:0>2d}".format(q), '', 1) for q in range(0,100)]

FailList=[]

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

SQL.execute("""drop table if exists failed""")
SQL.execute("""
        create table failed (
            problem text,
            team    text,
            solved  text);
          """)

SQL.execute("""drop table if exists bonus""")
SQL.execute("""
        create table bonus (
            problem text PRIMARY KEY,
            name    text,
            bonus   integer);
          """)

SQL.executemany('INSERT           into bonus values (?,?,?)', BonusPoints )
SQL.executemany('INSERT or IGNORE into bonus values (?,?,?)', DefaultPoints )

#setup is complete
SQLconn.commit()

#print('BonusPoints=',BonusPoints)

# Read in all the problems
for files in glob.glob(problemFiles+'*.[tT][xX][tT]'):
    file = files.split('/')[-1]
    # Split filename at the dash, get the problem number
    problem, team = file.split('.')[0].split('-')
    # if the filename has no problem number, continue to next file
    if not problem in [pnum for pnum,pname,ppt in BonusPoints]:
        continue

    solved  = os.path.getmtime(problemFiles+file)

    returncode = 0
    # Check for correct output
    try:
        x = subprocess.check_call(['diff','-w', '-B',
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
                SQL.execute("""UPDATE score 
                               SET solved = ? 
                               WHERE problem = ? and team = upper(?)""",
                    (solved, problem, team))
        SQLconn.commit()
    else:
        # track the failures
        sha256 = hashlib.sha256(open(problemFiles+file, 'rb').read()).hexdigest()
        os.rename(problemFiles+file,
                  problemFiles+problem+'-'+team+'-'+sha256+'.fail')

for files in glob.glob(problemFiles+'*.[fF][aA][iI][lL]'):
    solved  = os.path.getmtime(files)
    file = files.split('/')[-1]
    # Split filename at the dash, get the problem number
    problem, team, sha256 = file.split('.')[0].split('-')
    FailList.append((team,problem))
    SQL.execute("INSERT into failed values (?, upper(?), ?)", 
        (problem, team, solved))
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
    scorelist.append((bonus*row[3],row[0],row[1]))

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
                <meta http-equiv="refresh" content="''' + Refresh + '''">
                <link rel="stylesheet" href="''' + css + '''">
              </head>
              <body><div class="body">
        ''')
# First Div
f.write ("""<div class="left">""")
# Team score summary
f.write ("""<table><caption>""")
f.write (datetime.now().strftime('%m/%d&nbsp;%H:%M:%S'))
f.write ("""    <br>Team Scores""")
f.write ("""    </caption>
              <tr><th align="left">Team</th><th>Score</th><th>Pct</th></tr>
         """)

for row in SQL.execute("""SELECT  team, sum(score) as TeamScore,
                                        count(team) as Completed
                          FROM score
                          GROUP by team
                          ORDER by TeamScore desc"""):
    failCount = len([y for y in FailList if y[0].upper()==row[0]])
    f.write('<tr><td>'                 +     row[0]  + 
            '</td><td align="center">' + str(row[1]) +
            '</td><td align="center">' + '{:.1%}'.format(row[2]/(row[2]+failCount))+ 
            '</td></tr>')
#end the team score summary
f.write ("""</table>""")

# Failed Problems sorted by time 
f.write ("""<table><caption><br>Failed Attempts</caption>
            <tr><th>Problem</th>
            <th align="left">Team</th>
            <th>Time</th></tr>
         """)

for row in SQL.execute("""SELECT  problem, team, solved
                          FROM failed
                          ORDER by solved desc"""):
    f.write('</td><td align="center">'+     row[0]  + 
            '</td><td>'               + str(row[1]) + 
            '</td><td align="left";style="white-space:nowrap;">'+ 
             datetime.fromtimestamp(float(row[2])).strftime('%H:%M:%S') +
            '</td></tr>')
#end of Failed Problems sort by time
f.write ("""</table>""")

# end first div
f.write ("""</div>""")

# Problems summary table
f.write ("""  <div class="col"><table><caption><br>Problems Solved</caption>
              <tr><th align="left">Problem</th><th>Value</th><th>#</th></tr>
         """)

for row in SQL.execute("""SELECT score.problem || '-'  || bonus.name as problem,
                                 bonus.bonus, 
                                 count(score.problem) as countprob 
                          FROM score, bonus 
                          WHERE score.problem = bonus.problem 
                          GROUP by score.problem
                          ORDER by score.problem
                       """):

    f.write('</td><td align="left">' +     row[0]  + 
            '</td><td align="center">' + str(row[1]) + 
            '</td><td align="center">' + str(row[2]) + 
            '</td></tr>')
#end the problems summary table
f.write ("""</table></div>""")

# third div
f.write ("""  <div class="col"> """)

# Problems solved sorted by time 
f.write ("""<table><caption><br>Successful Submittals</caption>
            <tr><th>Problem</th>
            <th align="left">Team</th>
            <th>Time</th><th>Score</th></tr>
         """)

for row in SQL.execute("""SELECT  problem, team, solved, score
                          FROM score
                          ORDER by solved desc"""):
    f.write('</td><td align="center">'+     row[0]  + 
            '</td><td>'               + str(row[1]) + 
            '</td><td align="left";style="white-space:nowrap;">'+ 
             datetime.fromtimestamp(float(row[2])).strftime('%m-%d&nbsp;%H:%M:%S') +
            '</td><td align="center">'+ str(row[3]) + 
            '</td></tr>')
#end of Problems solved sort by time
f.write ("""</table>""")

# Third div
f.write ("""</div>""")

# end the html body
f.write ("""</div></body></html>""")

f.close()

# try to write the CSS, may fail if CSS is readonly
try:
    f = open(css, 'w')

    f.write ("""
div.body {
    width: 95%;
    margin-left: none;
    margin-right: none;
    margin-top: none;
    margin-bottom: none;
}

div.left {
    margin-right: 60px;
    float: left;
    width: 25%;
}

div.col {
    float: left;
    width: 33%;
}

body {
  font: 100% "Arial", sans-serif;
  color: #333;
  background: #F3F5F7;
}

table {
  font: 100% "Arial", sans-serif;
  border-width: 1px 1px 1px 1px;
  padding: 2;
  margin: 2;
  border-collapse: collapse;
  color: #333;
  background: #F3F5F7;
}

table caption {
  padding-bottom: 5px;
  font: 125% "Arial", sans-serif;
}

table thead th {
  background: #3A4856;
  padding: 1px 4px;
  color: #fff;
  text-align: left;
  font-weight: normal;
}

table tbody td, table tbody th {
    border-width: 2px 2px 2px 2px;
    border-style: groove groove groove groove ;
  padding: 2px 4px 2px 5px;
 }
""")

    f.close()
except PermissionError:
    pass

#close SQLite3
SQLconn.commit()
SQLconn.close()
