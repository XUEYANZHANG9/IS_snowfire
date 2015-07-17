#!/bin/bash 
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q
#$ -N prectemp


basins="cascades california northernrockies southernrockies whites"
#basins="southernrockies"
models="NorESM1-M CNRM-CM5 CSIRO-Mk3-6-0 CanESM2 MIROC5 bcc-csm1-1-m HadGEM2-CC365 HadGEM2-ES365 CCSM4 IPSL-CM5A-MR"
#scenarios="historical rcp45 rcp85"
scenarios="rcp45 rcp85" 

# /raid9/gergel/agg_snowpack/gcms_var
 
#### deal with years 


for basin in $basins
do
	for model in $models
	do
		for scenario in $scenarios
		do 
			#### and which scenario it is
			if [ "historical" = "${scenario}" ]
			then
			years="1950_2005"
			newyears="1970-1999"
			file_pr="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.monsum.pr.${years}_${basin}.nc"
                        file_swe="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.monday1.SWE.${years}_${basin}.nc"
			file_tempmax="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.monmean.tasmax.${years}_${basin}.nc"
			file_tempmin="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.monmean.tasmin.${years}_${basin}.nc"
			ofile_pr="/raid9/gergel/agg_snowpack/gcms_var/pr_${basin}_${model}_${scenario}_${newyears}.nc"
                        ofile_swe="/raid9/gergel/agg_snowpack/gcms_var/swe_${basin}_${model}_${scenario}_${newyears}.nc"
			ofile_tempmax="/raid9/gergel/agg_snowpack/gcms_var/tasmax_${basin}_${model}_${scenario}_${newyears}.nc"
			ofile_tempmin="/raid9/gergel/agg_snowpack/gcms_var/tasmin_${basin}_${model}_${scenario}_${newyears}.nc"
			cdo -selyear,1969/1999 $file_pr $ofile_pr
			cdo -selyear,1969/1999 $file_swe $ofile_swe
			cdo -selyear,1969/1999 $file_tempmax $ofile_tempmax
			cdo -selyear,1969/1999 $file_tempmin $ofile_tempmin
			echo "finished processing $basin $model for $scenario" 
			else
			years="2006_2099"
			newyears="2070-2099"
			file_pr="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.monsum.pr.${years}_${basin}.nc"
                        file_swe="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.monday1.SWE.${years}_${basin}.nc"
			file_tempmax="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.monmean.tasmax.${years}_${basin}.nc"
                        file_tempmin="/raid9/gergel/agg_snowpack/goodleap/${basin}/${model}__${scenario}.monmean.tasmin.${years}_${basin}.nc"
			ofile_pr="/raid9/gergel/agg_snowpack/gcms_var/pr_${basin}_${model}_${scenario}_${newyears}.nc"
                        ofile_swe="/raid9/gergel/agg_snowpack/gcms_var/swe_${basin}_${model}_${scenario}_${newyears}.nc"
			ofile_tempmax="/raid9/gergel/agg_snowpack/gcms_var/tasmax_${basin}_${model}_${scenario}_${newyears}.nc"
                        ofile_tempmin="/raid9/gergel/agg_snowpack/gcms_var/tasmin_${basin}_${model}_${scenario}_${newyears}.nc"
			cdo -selyear,2069/2099 $file_pr $ofile_pr
                        cdo -selyear,2069/2099 $file_swe $ofile_swe
			cdo -selyear,2069/2099 $file_tempmax $ofile_tempmax
			cdo -selyear,2069/2099 $file_tempmin $ofile_tempmin 
			echo "finished processing $basin $model for $scenario" 
			fi
		done 
	done
done 
