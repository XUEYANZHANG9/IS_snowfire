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
timecalc="monday1"
elif [ "pr" = "$variable" ] || [ "PET_NatVeg" = "$variable" ] || [ "PET_Short" = "$variable" ] || [ "PET_Tall" = "$variable" ] || [ "Transp" = "$variable" ] || [ "Evaporation" = "$variable" ]
then
timecalc="monsum"
else
timecalc="monmean"
fi

#### and which scenario it is
if [ "historical" = "$scenario" ]
then
years="1950-2005"
else
years="2006-2099"
fi

## /raid3/stumbaugh/IS/CONUS/share/monsumms-vic-gcm5I-livneh.20150123
#### filename
if [ "SWE" = "$variable" ]
then
inputfile="/raid3/stumbaugh/IS/CONUS/share/monsumms-vic-gcm10-livneh.20150127/${model}__${scenario}.${timecalc}.${variable}.${years}.nc"
elif [ "TotalSoilMoist" = "$variable" ] || [ "PET_NatVeg" = "$variable" ] || [ "PET_Short" = "$variable" ] || [ "PET_Tall" = "$variable" ] || [ "Transp" = "$variable" ] || [ "Evaporation" = "$variable" ]
then
inputfile="/raid3/stumbaugh/IS/CONUS/share/monsumms-vic-gcm10-livneh.20150127/${model}__${scenario}.${timecalc}.${variable}.${years}.nc"
else
inputfile="/raid3/stumbaugh/IS/CONUS/share/cat.WUS.summ.diana.patched/${model}_${scenario}_${variable}.${timecalc}.nc"
fi
tmp="/raid9/gergel/agg_snowpack/goodleap/tmp_${model}_${variable}_${scenario}.nc"
if [ "TotalSoilMoist" = "$variable" ]
then
outputfile="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.${timecalc}.${variable}.${years}_${basin}_august.nc"
else 
outputfile="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.${timecalc}.${variable}.${years}_${basin}.nc"
fi
# output="/raid9/gergel/agg_snowpack/goodleap/${model}_${scenario}_${variable}.${timecalc}.nc"
# grid="/raid9/gergel/agg_snowpack/forcinggridinfo.txt"

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
	cdo selmon,8 $inputfile $tmp
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

if [ "$basin" = "california" ]
then
        echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-122.5,-117,41.5,34.5 $tmp $outputfile
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
else [ "$basin" = "cascades" ]
        echo "now processing $inputfile with $basin mask"
        cdo masklonlatbox,-123.25,-119.5,49.0,41.5 $tmp $outputfile
fi
 
