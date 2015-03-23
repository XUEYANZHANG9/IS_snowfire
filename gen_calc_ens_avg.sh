#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N ens_avg

# variables="tasmax tasmin pr SWE"
variables="tasmax tasmin pr" 
basin="california whites northernrockies southernrockies cascades"
scenario="historical rcp45 rcp85"
models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
arr_mod=($models)
arr_bas=($basin)
arr_sc=($scenario)
arr_vars=($variables)

## loop over models
for var in 0 1 2  
do
	#### format of filename depends on which variable it is
	if [ "SWE" = "${arr_vars[$var]}" ]
	then
	timecalc="monday1"
	elif [ "pr" = "${arr_vars[$var]}" ]
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
			years="1950-2005"
			else
			years="2006-2099"
			fi

			for i in 0 1 2 3 4 5 6 7 8 9
			do 
				eval "ifile${i}="/raid9/gergel/agg_snowpack/goodleap/${arr_bas[$bas]}/${arr_mod[$i]}__${arr_sc[$scen]}.${timecalc}.${arr_vars[$var]}.${years}_${arr_bas[$bas]}.nc""
			done
			ofile="/raid9/gergel/agg_snowpack/goodleap/${arr_bas[$bas]}/${arr_vars[$var]}_ensavg_${arr_sc[$scen]}_${arr_bas[$bas]}.nc"
			## calculate ensemble mean
			echo "now calculating ensemble average for ${arr_vars[$var]} ${arr_bas[$bas]} ${arr_sc[$scen]}"
			cdo ensmean $ifile0 $ifile1 $ifile2 $ifile3 $ifile4 $ifile5 $ifile6 $ifile7 $ifile8 $ifile9 $ofile
		done 
	done
done

