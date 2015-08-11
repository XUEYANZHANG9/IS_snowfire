#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N thedonald 


python /raid9/gergel/agg_snowpack/p_t_dependence_30yr.py $type $basin $model $scenario 
