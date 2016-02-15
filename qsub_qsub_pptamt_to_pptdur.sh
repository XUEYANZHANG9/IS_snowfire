#!/bin/bash

basins="cascades california northernrockies southernrockies whites" 
models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
scenarios="historical rcp45 rcp85"

# basins="whites"
#models="CNRM-CM5"
#scenarios="historical"

### loop over basins
for model in $models
do
	for scenario in $scenarios
	do 
		echo "processing $model $scenario"
        	qsub -v model=$model,scenario=$scenario qsub_pptamt_to_pptdur.sh 
	done  
done

