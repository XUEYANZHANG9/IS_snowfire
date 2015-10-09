#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N lowlands


##-------------------------------------------------

################## sum up SWE 
if [ "$variable" = "pr" ] || [ "$variable" = "tasmax" ] || [ "$variable" = "tasmin" ]
then
python /raid9/gergel/agg_snowpack/summer_sm_uplow_lands.py $type $variable $basin $model $scenario $season
else
python /raid9/gergel/agg_snowpack/summer_sm_uplow_lands.py $type $variable $basin $model $scenario 
fi 
