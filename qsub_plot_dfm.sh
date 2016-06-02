#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N dfm_100
#$ -m abe
#$ -M gergel@uw.edu 

source /home/gergel/.bashrc
source activate /home/gergel/anaconda/envs/my_env

# python plot_1000hr_dfm.py 

python plot_100hr_dfm.py 
