#!/bin/bash

#################### INPUT ARGUMENT: VARIABLE,BASIN,MODEL,SCENARIO  ############################################################################

## /home/raid9/gergel/agg_snowpack

variable=$1
basin=$2
model=$3
scenario=$4

#### format of filename depends on which variable it is
if [ "SWE" = "$variable" ]
then
timecalc="monday1"
elif [ "TotalSoilMoist" = "$variable" ]
then
#timecalc="monday1"
timecalc="monmean" ## changed for average soil moisture 
elif [ "pr" = "$variable" ] || [ "petNatVeg" = "$variable" ] || [ "petShort" = "$variable" ] || [ "petTall" = "$variable" ] || [ "Transp" = "$variable" ] || [ "Evaporation" = "$variable" ]
then
timecalc="monsum"
else
timecalc="monmean"
fi

if [ "CCSM4" = "$model" ] 
then
modnum="r6i1p1"
else
modnum="r1i1p1"
fi 

#### and which scenario it is
if [ "historical" = "$scenario" ]
then
years="1950_2005"
else
years="2006_2099"
fi


#### filename
if [ "pr" = "$variable" ] || [ "tasmin" = "$variable" ] || [ "tasmax" = "$variable" ] 
then
inputfile="/raid9/gergel/agg_snowpack/is_summ/cat.WUS.summ.diana.tight/${model}_${scenario}_${variable}.${timecalc}.nc" 
else
inputfile="/raid9/gergel/agg_snowpack/is_summ/${model}_${modnum}_${scenario}_monthly.rec/vic_${variable}_${model}_${modnum}_${scenario}_${years}_WUSA_monthly_${timecalc}.nc"
fi 

tmp="/raid9/gergel/agg_snowpack/goodleap/tmp_${model}_${variable}_${scenario}.nc"

if [ "TotalSoilMoist" = "$variable" ]
then
outputfile="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.${timecalc}.${variable}.${years}_${basin}_summer.nc"
else 
outputfile="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.${timecalc}.${variable}.${years}_${basin}.nc"
fi


###################################### RUN THIS PART TO REGRID FORCING FILES AND COMMENT OUT THE BOTTOM CDO PART #############################################################

## reset grid from generic to latlon 
## cdo setgrid,$grid $inputfile $output


##############################################################################################################################################################################
#### lat lon boundaries depend on mtn range

if [ "$variable" = "SWE" ]
then
        cdo selmon,4 $inputfile $tmp
elif [ "$variable" = "TotalSoilMoist" ]
then
	cdo selmon,6,7,8 $inputfile $tmp
elif [ "$variable" = "pr" ]
then
        cdo selmon,11,12,1,2,3 $inputfile $tmp
elif [ "$variable" = "tasmax" ]
then
	cdo selmon,11,12,1,2,3 $inputfile $tmp
elif [ "$variable" = "tasmin" ]
then
	cdo selmon,11,12,1,2,3 $inputfile $tmp
else
	echo "the entire year is needed for this variable,so tmp = inputfile" 
	tmp=$inputfile 
fi

if [ "$basin" = "nwinterior" ]
then
        echo "now processing $inputfile with $basin mask"
        outputfile=$tmp
elif [ "$basin" = "coastalnorth" ]
then
        echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-124.5,-122,48,41.5 $tmp $outputfile
elif [ "$basin" = "coastalsouth" ]
then
        echo "now processing $inputfile with $basin mask"
	outputfile=$tmp
elif [ "$basin" = "missouri" ]
then
        echo "now processing $inputfile with $basin mask"
        outputfile=$tmp
elif [ "$basin" = "great_basin" ]
then
        echo "now processing $inputfile with $basin mask"
        outputfile=$tmp
elif [ "$basin" = "lower_colorado"]  
then
	echo "now processing $inputfile wtih $basin mask"
	outputfile=$tmp
else
	echo "the wrong basin name was entered as input"
fi
 
