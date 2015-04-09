#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N petaet


##-------------------------------------------------

python /raid9/gergel/agg_snowpack/calc_moist_deficit.py $basin $scenario 
