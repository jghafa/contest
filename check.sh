#!/bin/bash 
#Parameter 1 is the directory for solution files

#-xv
#trap read debug

#Housekeeping
# make array empty when no matches
shopt -s nullglob

# Note the time
now=$(date +"%T")

#log file name
lname=$(date +"%m-%d-%ycontest.log")

# Make sure answers exist
if [ -d "answers" ]; 
then
  echo 
  answers=(./answers/[0-9][0-9]*.txt)
  echo ${#answers[@]} 'Answers files loaded'
  if [ ${#answers[@]} -eq 0 ]; 
  then
    echo 'No answers were detected in the answers directory'
    exit
  fi  
else   # dir does not exist,so make it and create the example file
  echo 'answers exist' 
  mkdir answers
  echo 42 > answers/00.txt
  echo 'Directory answers created, please fill with answer files.'
  echo 'File name format: 00.txt for the answer to question 0'
  exit
fi

#echo
#echo parameters $# $1 $2 $3
#echo files
#echo $1*.txt

# Read the files names from the specified directory
array=($1[0-9][0-9]*.txt)
echo
echo ${#array[@]} 'Files submitted for review' 
#echo 'files found'
#echo "${array[@]}" # echo file names
#echo 

#Check each file
for i in "${array[@]}"
do
# get first chars from file name, use to get answer file
  j="${i:${#1}:2}"   # Extract problem number, skip param 1 length, then get 2
  diff -w $i ./answers/${j}.txt > /dev/null
  if [ $? -ne 0 ]; then    # did it match
    echo $i 'did not match'| tee -a $lname
  else
    echo $i 'Matched' $now | tee -a $lname
  fi
done
#echo direct ${array[0]}
#echo direct ${array[1]}

