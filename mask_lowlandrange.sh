#!/bin/bash

#################### INPUT ARGUMENT: VARIABLE,BASIN,MODEL,SCENARIO  ############################################################################

## /home/raid9/gergel/agg_snowpack

variable=$1
basin=$2
model=$3
scenario=$4
season=$5
 

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
outputfile="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.${timecalc}.${variable}.${years}_${basin}_${season}.nc"
fi


###################################### RUN THIS PART TO REGRID FORCING FILES AND COMMENT OUT THE BOTTOM CDO PART #############################################################

## reset grid from generic to latlon 
## cdo setgrid,$grid $inputfile $output


##############################################################################################################################################################################
#### lat lon boundaries depend on mtn range

if [ "$variable" = "TotalSoilMoist" ] && [ "$basin" = "coastalnorth" ] 
then
	cdo selmon,6,7,8 $inputfile $tmp
elif [ "$variable" = "TotalSoilMoist" ] && [ "$basin" != "coastalnorth" ]
then
	echo "now processing $inputfile with cdo selmon" 
	cdo selmon,6,7,8 $inputfile $outputfile 

elif [ "$variable" = "pr" ] && [ "$basin" = "coastalnorth" ] || [ "$basin" = "cascades" ] || [ "$basin" = "california" ] || [ "$basin" = "northernrockies" ] || [ "$basin" = "southernrockies" ] || [ "$basin" = "whites" ] 
then
	if [ "$season" = "mam" ]
	then
	echo "processing $inputfile with mam"
	cdo selmon,3,4,5 $inputfile $tmp
	else
	echo "processing $inputfile with jja"
	cdo selmon,6,7,8 $inputfile $tmp 
	fi 

elif [ "$variable" = "pr" ] && [ "$basin" != "coastalnorth" ] 
then
	if [ "$season" = "mam" ]
        then
        echo "processing $inputfile with $basin mam"
        cdo selmon,3,4,5 $inputfile $outputfile
        else
        echo "processing $inputfile with $basin jja"
        cdo selmon,6,7,8 $inputfile $outputfile
        fi
fi

if [ "$basin" = "coastalnorth" ]
then
        echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-124.5,-122,48,41.5 $tmp $outputfile
elif [ "$basin" = "northernrockies" ]
then
        echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-119.5,-107.5,49.0,42.37 $tmp $outputfile
elif [ "$basin" = "southernrockies" ]
then
        echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-113.0,-104.0,42.37,35.0 $tmp $outputfile
elif [ "$basin" = "whites" ]
then
        echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-111,-108,36,32 $tmp $outputfile
elif [ "$basin" = "cascades" ]
then
        echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-123.25,-119.5,49.0,41.5 $tmp $outputfile
elif [ "$basin" = "california" ] 
then 
	echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-122.5,-117,41.5,34.5 $tmp $outputfile
fi
 
