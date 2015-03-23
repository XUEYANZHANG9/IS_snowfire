#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N b_rock


##-------------------------------------------------

################## sum up SWE 

######### input args come from command line of qsub in qsub_qsub script
################# WITH LEAP YEARS
## python /raid9/gergel/agg_snowpack/qsub_latlon_adjusted_basin_aggregated_snowpack.py $basin $model $scenario

################ WITHOUT LEAP YEARS
# python /raid9/gergel/agg_snowpack/basin_aggregated_snowpack_debug_latlonnum_wout_leap_yrs.py $basin $model $scenario 

python /raid9/gergel/agg_snowpack/sum_up_swe_compare_months.py $basin $model $scenario 
