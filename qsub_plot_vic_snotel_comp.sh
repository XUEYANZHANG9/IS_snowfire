#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N  tbt

#basins="california southernrockies northernrockies whites cascades"
basins="california"

for basin in $basins
do
        python /raid9/gergel/agg_snowpack/plot_vic_snotel_comp.py $basin
done

