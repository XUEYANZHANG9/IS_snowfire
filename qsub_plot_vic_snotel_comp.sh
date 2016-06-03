#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N thnkgditsfrday

#basins="california southernrockies northernrockies whites cascades"
#basins="california"

#for basin in $basins
#do
#        python /raid9/gergel/agg_snowpack/plot_vic_snotel_comp.py $basin
#done

python plot_lp_elev_vic_snotel_comp.py 
