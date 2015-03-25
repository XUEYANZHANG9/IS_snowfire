#!/bin/bash

# basins="cascades california northernrockies southernrockies" 
# models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
# scenarios="historical rcp45 rcp85"

basins="california"
# models="MIROC5"
scenarios="historical"

### loop over basins
for basin in $basins
do
        for scenario in $scenario
        do
                echo "processing %basin %scenario" 
		qsub -v basin=$basin,scenario=$scenario qsub_grid_cell_elevation_mean.sh
        done
done

