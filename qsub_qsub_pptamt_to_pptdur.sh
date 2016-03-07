#!/bin/bash

models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
scenarios="historical rcp45 rcp85"
#variables="tmin tmax rh pptdur" 

#models="CNRM-CM5"
#scenarios="historical"
variables="pptdur"

### loop over basins
for variable in $variables
do 
	for model in $models
	do
		for scenario in $scenarios
		do 
			echo "processing $variable $model $scenario"
        		qsub -v variable=$variable,model=$model,scenario=$scenario qsub_pptamt_to_pptdur.sh 
			#python /raid9/gergel/agg_snowpack/slice_dfm_inputs.py $variable $model $scenario
		done  
	done 
done

