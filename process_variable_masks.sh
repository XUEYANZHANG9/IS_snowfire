#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N et


##-------------------------------------------------

models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
scenarios="historical rcp45 rcp85"
basins="california cascades northernrockies southernrockies whites" 
# variables="tasmax tasmin pr PET_NatVeg PET_Short PET_Tall Transp Evaporation"
variables="PET_NatVeg PET_Short PET_Tall Transp Evaporation"
# models="bcc-csm1-1-m CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 CCSM4"

for variable in $variables
do
        for basin in $basins
        do
                for model in $models 
		do 
			for scenario in $scenarios 
			do 
				/raid9/gergel/agg_snowpack/mask_mtnrange.sh $variable $basin $model $scenario
        		done
		done
	done	
done	

