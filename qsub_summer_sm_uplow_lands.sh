#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q interactive.q
#$ -N sm_lowlands


##-------------------------------------------------

python /raid9/gergel/agg_snowpack/summer_sm_uplow_lands.py $basin $scenario 
