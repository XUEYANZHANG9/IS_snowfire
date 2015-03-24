#!/bin/bash

basins="cascades california northernrockies southernrockies whites" 
#models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
scenarios="historical rcp45 rcp85"

#basins="northernrockies"
# models="IPSL-CM5A-MR"
#scenarios="historical"



### loop over basins
for basin in $basins
do
        for scenario in $scenarios
        do
                echo "processing $basin $scenario"
		qsub -v basin=$basin,scenario=$scenario qsub_sum_swe.sh
        done
done

