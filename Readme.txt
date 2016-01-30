The Python script score.py3 is built to judge answers in a programming contest, score them according to the contest rules, and display the scores in a HTML/CSS page.

A web server is not needed.  The HTML/CSS can be hosted in a local file and the browser will automatically refresh to display updated files.

The Python script rebuilds a SQLite3 database with each run.  The database is retained after the script finishes.

The file score.ini configures the program, allowing you to set file path names and set the scores awarded for each problem.

The correct answers are contained in "AnswerFiles" parameter in score.ini.  These answers require a specific filename format.  For instance, the filename 00.txt holds the answer for question 0.

The contestants answers are stored in "ProblemFiles" parameter in score.ini.  Again, a specific filename format is required.  For instance, the filename 00-Team A.txt contains Team A submittal for problem 00.  The script uses the first two digits to find the answer file, and then uses "DIFF -w" to compare the two files.  Mixed case is allowed, and the script considers "TEAM A" and "team a" to be the same team.


