#!/bin/bash 

#types="ensavg eachgcm"
basins="cascades california northernrockies southernrockies whites"
scenarios="historical rcp45 rcp85"
models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"

types="ensavg"
#models="CanESM2"
#basins="northernrockies"
#scenarios="rcp45"

for type in $types 
do
	if [ "ensavg" = "$type" ]
	then
	### loop over basins
	for basin in $basins 
	do 
		for scenario in $scenarios
		do
			echo "processing $type $basin $scenario" 
			qsub -v type=$type,basin=$basin,scenario=$scenario qsub_p_t_dependence.sh 
		done
	done 
	
	elif [ "eachgcm" = "$type" ]
	then 
	## loop over basins
	for basin in $basins
	do
		## loop over models
		for model in $models
		do
			## loop over scenarios
			for scenario in $scenarios
			do
				echo "processing $type $basin $model $scenario" 
				qsub -v type=$type,basin=$basin,model=$model,scenario=$scenario qsub_p_t_dependence_gcms.sh 
			done
		done
	done

	fi 
done 
