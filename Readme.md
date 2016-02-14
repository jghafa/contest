#Programming Contest Scoring Documentation

##Overview of score.py3
The Python script score.py3 is built to judge answers in a programming contest, score them according to the contest rules, and display the scores in a HTML/CSS page.

All problems in the programming contest are based on text files.  Input is from text files, the teams submit answers on text files, and the team answers are compared to a reference text file using the unix command "diff -w".

The HTML/CSS are hosted in a local file, and a web server is not needed.  The HTML file will automatically refresh to display updated results as they are run.  The ini file controls the refresh time.

The Python script rebuilds a SQLite3 database with each run.  The database is retained after the script finishes as the record of the contest.


##Overview of trans.py3
The Python script trans.py3 quickly moves progam submissions on game day. It moves selected files from the submitting USB drive to designated folder.  The folders are specified in the scores.ini file.
It can be called via a right-click in the file browser.


##Overview of contestfiles.p3y
The Python script contestfiles.py3 quickly moves problem descriptions, program input, and contest rules to a designated folder. The folders are specified in the scores.ini file.
It can be called via a right-click in the file browser.


##Filename Descriptions
Submitted answers and reference answer must follow a specific file name pattern.  The AnswerFiles are our correct, expected answer.  ProblemFiles are the team's submitted answers.

###AnswerFiles 
Contain the correct reference answer and follow this pattern:  **"00.txt"**.
The first two charactors indicate the problem number, followed by **".txt"**.

###ProblemFiles 
Contain the team's answer and must follow this patter: **"00-Team A.txt"**.
The first two charactors indicate the problem number.
The characters between the **"-"** and the **".txt"** indicate the team name.
In the example, the team name is "Team A" and they have submitted an answer for problem 00.

The script considers "TEAM A" and "team a" to indicate the same team.


##Initialization File Description
The file score.ini configures the program, allowing you to set file path names and set the scores awarded for each problem.

The [Paths] section of score.ini sets file paths:

###AnswerFiles
Sets the directory path to the correct reference answers.  For example:

`AnswerFiles=../2016Problems/JGH-answers/answers/`

###ProblemFiles 
Sets the directory path to the contestants answers.  For example:

`ProblemFiles=../2016Problems/JGH-answers/`

###HTMLOutput
Sets the path to the contest summary web page.  This file is overwritten with each run of the program.  For example:

`HTMLOutput=/home/jghafa/scores.html`

###cssOutput
Sets the path to the HTML CSS file.  This file is overwritten with each run of the program.  However, if the css file is marked readonly the script does not attempt a re-write.

`cssOutput=/home/jghafa/scores.css`

###logOutput
Location of the log file. The log files tracks script submissions, and logs errors.

`/home/jghafa/scores.log`

###scoreProg
The location of the scoring script.  The transfer script invokes the score script to update the web page.

`/home/jghafa/contest/score.py3`

###TeamHandouts
The location of problems and inputs to give to the teams.  contestfiles.py3 uses this.

`/home/jghafa/2016Problems/`

###HandoutDir
The new directory on USB drives that will get the problem descriptions and inputs.

`ContestFiles2016/`



The [Bonus] section of score.ini controls the score assigned to a problem.
If this section is left blank, all problems have a base score of 1.

###Problems
The list of problem names

`Problems=01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19`

###Points
The associated points for the list above.

`Points=1,2,3,4,10,10,10,3,5,10,7,4,3,8,9,10,7,3,5`

If a problem is not listed in the Bonus section, it gets the default score of 1.
