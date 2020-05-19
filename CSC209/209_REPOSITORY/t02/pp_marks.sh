#!/bin/bash

declare -i assign_total_max=0
declare -i assign_total_score=0
declare -i tut_total_max=0
declare -i tut_total_score=0

for d in a1 a2 a3 a4; do 

if [ -d ./$d ] && [ -e ./$d/feedback.txt ];
then
 grade=$(tail -n 1 $d/feedback.txt)
 #grade=`cat $d/feedback.txt | tr -d [:blank:]`

 IFS='/' read -ra grArray <<< "$grade"
 score=${grArray[0]}
 max=${grArray[1]}
 echo $d: $score / $max
 assign_total_max=assign_total_max+max
 assign_total_score=assign_total_score+score

else
 echo $d: "- / -"
fi
done

echo

for d in t01 t02 t03 t04 t05 t06 t07 t08 t09 t10 t11; do
if [ -d ./$d ] && [ -e ./$d/feedback.txt ];
then
 grade=$(tail -n 1 $d/feedback.txt)
 #grade=`cat $d/feedback.txt | tr -d [:blank:]`

 IFS='/' read -ra grArray <<< "$grade"
 score=${grArray[0]}
 max=${grArray[1]}
 echo $d: $score / $max
 tut_total_max=tut_total_max+max
 tut_total_score=tut_total_score+score

else
 echo $d: "- / -"
fi
done

echo
echo "Assignment Total: "$assign_total_score / $assign_total_max
echo "Tutorial Total: "$tut_total_score / $tut_total_max
