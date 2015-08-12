#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N precip_mtns


##-------------------------------------------------
seasons="mam jja" 
models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
scenarios="historical rcp45 rcp85"
#scenarios="rcp45"
#basins="nwinterior coastalnorth coastalsouth missouri lower_colorado great_basin"  
basins="cascades california northernrockies southernrockies whites"
variables="pr"
#variables="SWE tasmax tasmin pr TotalSoilMoist petNatVeg petShort petTall Transp Evaporation"
#models="CNRM-CM5"
season="junk"

for variable in $variables
do
        if [ "pr" = "$variable" ]
	then 
	## loop over seasons
	for season in $seasons
	do
		## loop over basins
		for basin in $basins
        	do
                	## loop over models 
			for model in $models 
			do 
				## loop over scenarios
				for scenario in $scenarios 
				do 
					/raid9/gergel/agg_snowpack/mask_lowlandrange.sh $variable $basin $model $scenario $season
        			done
			done
		done	
	done	

	elif [ "TotalSoilMoist" = "$variable" ] 
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
					/raid9/gergel/agg_snowpack/mask_lowlandrange.sh $variable $basin $model $scenario $season 
			done
		done
	done

	fi 
done 
