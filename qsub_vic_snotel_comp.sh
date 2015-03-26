#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N kettlemans 


upper_lats=("41.5")
lower_lats=("35.5")
left_lons=("-122.5")
rt_lons=("-118")

for i in 0 
do
	python /raid9/gergel/agg_snowpack/vic_snotel_comparison.py ${upper_lats[$i]} ${lower_lats[$i]} ${left_lons[$i]} ${rt_lons[$i]}
done

