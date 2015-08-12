#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q@compute-0-2.local 
#$ -N sm_gcms


##-------------------------------------------------

################## sum up SWE 
if [ "$variable" = "pr" ]
then
python /raid9/gergel/agg_snowpack/summer_sm_uplow_lands.py $type $variable $basin $model $scenario $season
else
python /raid9/gergel/agg_snowpack/summer_sm_uplow_lands.py $type $variable $basin $model $scenario 
fi 
