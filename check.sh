#!/bin/bash
# make array empty when no matches
shopt -s nullglob
#echo
#echo start
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

