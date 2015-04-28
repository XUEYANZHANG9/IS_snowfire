#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q interactive.q
#$ -N elevplot 

python /raid9/gergel/agg_snowpack/elev_bins.py 


