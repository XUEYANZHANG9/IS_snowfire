#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q interactive.q
#$ -N fpn100
#$ -m abe 
#$ -M gergel@uw.edu 

source /home/gergel/.bashrc
source activate /home/gergel/anaconda/envs/my_env

#python plot_summer_sm.py 

# python plot_1000_fpn.py 

python plot_100_fpn_rev.py 

#python plot_1000_fpn_rev.py 
