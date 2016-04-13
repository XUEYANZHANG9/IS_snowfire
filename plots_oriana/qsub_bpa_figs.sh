#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q 
#$ -N figs

source /home/gergel/.bashrc 

python /raid9/gergel/agg_snowpack/plots_oriana/bpa_figs.py $gcm $scenario $variable
