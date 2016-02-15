#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N pptdur

source /home/gergel/.bashrc
source activate /home/gergel/anaconda/envs/my_env

python /raid9/gergel/agg_snowpack/pptamt_to_pptdur.py $model $scenario

