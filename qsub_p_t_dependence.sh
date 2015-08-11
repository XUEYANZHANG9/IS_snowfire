#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q@compute-0-0.local
#$ -N hector_salamanca

python /raid9/gergel/agg_snowpack/p_t_dependence_30yr.py $basin $scenario 
