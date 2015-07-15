#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N kettlemans 

basins=("california" "southernrockies" "northernrockies" "whites" "cascades")
upper_lats=("41.5" "42.37" "49.0" "36" "49.0")
lower_lats=("34.5" "35.0" "42.37" "32" "41.5")
left_lons=("-122.5" "-113.0" "-119.5" "-111" "-123.25")
rt_lons=("-117" "-104.0" "-107.5" "-108" "-119.5")

for i in 0 1 2 3 4 
do
	python /raid9/gergel/agg_snowpack/vic_snotel_comparison.py ${basins[$i]} ${upper_lats[$i]} ${lower_lats[$i]} ${left_lons[$i]} ${rt_lons[$i]}
done

