#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q interactive.q
#$ -N fpn_100

source /home/gergel/.bashrc
source activate /home/gergel/anaconda/envs/my_env

#python plot_summer_sm.py 

# python plot_1000_fpn.py 

python plot_100_fpn_rev.py 
