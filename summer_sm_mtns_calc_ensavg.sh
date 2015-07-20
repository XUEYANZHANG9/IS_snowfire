#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q interactive.q
#$ -N ensavg_sm_mtns

#variables="SWE tasmin tasmax TotalSoilMoist pr petNatVeg petShort petTall Transp Evaporation"
variables="TotalSoilMoist" 
basin="california whites northernrockies southernrockies cascades"
scenario="historical rcp45 rcp85"
models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
arr_mod=($models)
arr_bas=($basin)
arr_sc=($scenario)
arr_vars=($variables)

## loop over models
for var in 0 
do
	#### format of filename depends on which variable it is
	if [ "SWE" = "${arr_vars[$var]}" ]
	then
	timecalc="monday1"
	elif [ "TotalSoilMoist" = "${arr_vars[$var]}" ]
	then
	timecalc="monmean"
	elif [ "pr" = "${arr_vars[$var]}" ] || [ "PET_NatVeg" = "${arr_vars[$var]}" ] || [ "PET_Short" = "${arr_vars[$var]}" ] || [ "PET_Tall" = "${arr_vars[$var]}" ] || [ "Transp" = "${arr_vars[$var]}" ] || [ "Evaporation" = "${arr_vars[$var]}" ]
	then
	timecalc="monsum"
	else
	timecalc="monmean"
	fi

	for bas in 0 1 2 3 4
	do 
		for scen in 0 1 2 
		do
			#### and which scenario it is
			if [ "historical" = "${arr_sc[$scen]}" ]
			then
			years="1950_2005"
			else
			years="2006_2099"
			fi
 				
			ifile1="/raid9/gergel/agg_snowpack/goodleap/${arr_bas[$bas]}/${arr_vars[$var]}_ensavg_${arr_sc[$scen]}_${arr_bas[$bas]}_june.nc"
			ifile2="/raid9/gergel/agg_snowpack/goodleap/${arr_bas[$bas]}/${arr_vars[$var]}_ensavg_${arr_sc[$scen]}_${arr_bas[$bas]}_july.nc"
			ifile2="/raid9/gergel/agg_snowpack/goodleap/${arr_bas[$bas]}/${arr_vars[$var]}_ensavg_${arr_sc[$scen]}_${arr_bas[$bas]}_august.nc"			


			ofile="/raid9/gergel/agg_snowpack/goodleap/${arr_bas[$bas]}/${arr_vars[$var]}_ensavg_${arr_sc[$scen]}_${arr_bas[$bas]}_summer.nc"
			## calculate ensemble mean
			echo "now calculating ensemble average for ${arr_vars[$var]} ${arr_bas[$bas]} ${arr_sc[$scen]}"
			cdo ensmean $ifile1 $ifile2 $ifile3 
		done 
	done
done

