#!/bin/bash

#gcms="CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 GFDL-ESM2M HadGEM2-CC HadGEM2-ES CCSM4 IPSL-CM5A-MR inmcm4"
#scenarios="rcp45 rcp85"
#variables="Runoff SWE Evaporation"

gcms="CNRM-CM5"
scenarios="rcp45"
variables="SWE" 

for gcm in $gcms
do
	for scenario in $scenarios
	do
        	for variable in $variables
		do
			echo "processing $gcm $scenario $variable"
			qsub -v gcm=$gcm,scenario=$scenario,variable=$variable qsub_bpa_figs.sh
		done
	done
done

