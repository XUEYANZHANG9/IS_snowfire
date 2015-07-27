#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q@compute-0-0.local 
#$ -N sm_gcms


##-------------------------------------------------

################## sum up SWE 

python /raid9/gergel/agg_snowpack/summer_sm_uplow_lands.py $type $basin $model $scenario 
