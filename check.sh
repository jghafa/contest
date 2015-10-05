#!/bin/bash 
#-xv
#trap read debug

#Housekeeping
# make array empty when no matches
shopt -s nullglob


# Make sure answers exist
if [ -d "answers" ] ; then
  echo answers exist
  answers=(./answers/[0-9][0-9]*.txt)
  echo number of answer files ${#answers[@]} 
  if [ ${#answers[@]} -eq 0 ]; then
    echo No answers were detected in the answers directory
    exit
  fi  
else
echo if false
  mkdir answers
  echo Directory 'answers' created, please fill with answer files.
  echo File name format: 00.txt for the answer to question 0
  exit
fi

#echo
#echo start
exit

#echo parameters $# $1 $2 $3
#echo files
#echo $1*.txt

array=($1*.txt)
echo
echo number of elements ${#array[@]} 
#echo elements
echo "${array[@]}" # echo elements
echo 

for i in "${array[@]}"
do
  diff $i ./answers/0.txt > /dev/null
  if [ $? -ne 0 ]; then    # did it match
    echo $i did not match          # nope
  else
    echo $i Matched
  fi
done
#echo direct ${array[0]}
#echo direct ${array[1]}

