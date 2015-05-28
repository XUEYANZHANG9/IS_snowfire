#!/bin/bash 

variables="pr temp"
#variables="temp"
chunks="1970-1999 2010-2039 2040-2069 2070-2099 2010-2039 2040-2069 2070-2099"
#chunks="2040-2069 2070-2099" 
scenarios="historical rcp45 rcp45 rcp45 rcp85 rcp85 rcp85"
#scenarios="rcp85 rcp85" 
basins="california cascades northernrockies southernrockies whites"
#basins="southernrockies" 
arr_ch=($chunks)
arr_sc=($scenarios)

## ${arr_ch[$ch]}
## ${arr_sc[$ch]}

## loop over variables 
for var in $variables  
do 
	## loop over scenarios and time chunks
	for ch in 0 1 2 3 4 5 6
	#for ch in 0 1 
	do
		## loop over basins
		for basin in $basins
		do
			echo "processing $var ${arr_ch[$ch]} ${arr_sc[$ch]} $basin" 
			qsub -hold_jid 3899805 -v variable=$var,chunk=${arr_ch[$ch]},scenario=${arr_sc[$ch]},basin=$basin qsub_pre_plot_climatology.sh 
		done
	done
done 


			

