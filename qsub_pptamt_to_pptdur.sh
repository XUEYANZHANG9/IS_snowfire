#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N elevs

source /home/gergel/.bashrc
source activate /home/gergel/anaconda/envs/my_env

# python /raid9/gergel/agg_snowpack/pptamt_to_pptdur.py $model $scenario

python /raid9/gergel/agg_snowpack/elevations_for_dfm.py

#python /raid9/gergel/agg_snowpack/slice_dfm_inputs.py $variable $model $scenario  
