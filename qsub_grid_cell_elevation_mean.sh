#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N loess


##-------------------------------------------------

################# swe elevation means 
# python /raid9/gergel/agg_snowpack/rev_grid_cell_elevation_mean.py $basin $model $scenario

#python /raid9/gergel/agg_snowpack/swe_elevation_slope2.py $basin 

python /raid9/gergel/agg_snowpack/loess_gridcell_elevation.py $basin $scenario 
