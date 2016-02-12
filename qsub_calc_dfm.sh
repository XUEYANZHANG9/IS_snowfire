#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q 
#$ -N dfm

# which python 
source /home/gergel/.bashrc 
# source activate /home/gergel/anaconda/envs/my_env 

python /raid9/gergel/agg_snowpack/calc_dfm_gridcell_is.py  
