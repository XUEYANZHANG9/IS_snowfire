#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q interactive.q@compute-0-1.local 
#$ -N clim

python /raid9/gergel/agg_snowpack/pre_plot_climatology.py $variable $chunk $scenario $basin 


