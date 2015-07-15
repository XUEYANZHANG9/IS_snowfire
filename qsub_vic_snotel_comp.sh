#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N kettlemans 

basins=("california" "southernrockies" "northernrockies" "whites" "cascades")
upper_lats=("41.5" "42.37" "49.0" "36" "49.0")
lower_lats=("35.5" "35.0" "42.0" "32" "41.5")
left_lons=("-122.5" "-112.5" "-117.0" "-111" "-123.25")
rt_lons=("-118" "-105.5" "-107.5" "-109" "-120")

for i in 0 1 2 3 4 
do
	python /raid9/gergel/agg_snowpack/vic_snotel_comparison.py ${basins[$i]} ${upper_lats[$i]} ${lower_lats[$i]} ${left_lons[$i]} ${rt_lons[$i]}
done

