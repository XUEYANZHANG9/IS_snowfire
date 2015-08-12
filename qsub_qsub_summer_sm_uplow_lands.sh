#!/bin/bash

#types="ensavg eachgcm" 
basins="cascades california northernrockies southernrockies whites nwinterior coastalnorth coastalsouth missouri lower_colorado great_basin" 
#basins="nwinterior coastalnorth coastalsouth missouri lower_colorado great_basin" 
models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
scenarios="historical rcp45 rcp85"
seasons="mam jja" 

types="eachgcm"
#basins="cascades"
#models="IPSL-CM5A-MR"
#scenarios="rcp45"
#seasons="mam"

################################ SET VARIABLE ########################
variable="pr"
######################################################################

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
			qsub -v type=$type,basin=$basin,scenario=$scenario qsub_summer_sm_uplow_lands.sh 
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
				if [ "$variable" = "pr" ]
				then
				for season in $seasons
				do
                                	echo "processing $type $variable $basin $model $scenario $season"
                                	qsub -v type=$type,variable=$variable,basin=$basin,model=$model,scenario=$scenario,season=$season qsub_summer_uplowlands_gcms.sh
                        	done
				else
				echo "processing $type $variable $basin $model $scenario"
                                qsub -v type=$type,variable=$variable,basin=$basin,model=$model,scenario=$scenario qsub_summer_uplowlands_gcms.sh
				fi
			done
                done
        done
	fi
done  
	

