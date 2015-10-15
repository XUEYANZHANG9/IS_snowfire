#!/bin/python 

import numpy as np
import math
import sys
import os
import pandas as pd
from snowpack_functions import mask_out_other_mtns,historical_sum_swe,unpack_netcdf_file_var 

def subtract_min_sm(ts_scen,ts_historical):
	min_in_storage = np.min(ts_historical)
	ts_minus_min = ts_scen - min_in_storage
	return(ts_minus_min) 

def create_gridcell_area_array(arr,lats,lons):
	import numpy as np
	resol = 0.0625 ## 1/16th degree resolution
	from snowpack_functions import calc_area
	vecfunc_calc_area = np.vectorize(calc_area) 
	return(vecfunc_calc_area(lats,lons,resol)) 
def create_mask_mtn_ranges(arr,lats,lons):
	import numpy as np
	from snowpack_functions import mask_out_other_mtns
	for j in np.arange(len(lats)):
		for k in np.arange(len(lons)):
			arr[0,j,k] = mask_out_other_mtns(lats[j],lons[k])
	return(arr) 


## get input arguments 
args=sys.argv[1:]
type = args[0] 
variable=args[1]
basin = args[2]
if (type == "ensavg"):
	scenario = args[3]
else: 
	model = args[3]
	scenario = args[4] 
if (variable == "pr") or (variable == "tasmin") or (variable == "tasmax"):
	season = args[5]
else:
	season = "summer"
if (scenario == "historical"):
	years = "1950_2005"
else:
	years = "2006_2099"
if (model == "CCSM4"):
	modnum = "r6i1p1"
else:
	modnum = "r1i1p1"
if (variable == "pr"):
	monthcalc = "monsum"
else:
	monthcalc = "monmean"

## import data 
#direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin 
#if (basin == "missouri") or (basin == "coastalsouth") or (basin == "lower_colorado") or ("basin == nwinterior") or ("basin == great_basin"):
#	direc = '/raid9/gergel/agg_snowpack/is_summ/%s_%s_%s_monthly.rec' % (model,modnum,scenario)
#	hist_direc = '/raid9/gergel/agg_snowpack/is_summ/%s_%s_%s_monthly.rec' % (model,modnum,"historical")
#	filename = 'vic_TotalSoilMoist_%s_%s_%s_%s_WUSA_monthly_monmean.nc' % (model,modnum,scenario,years) 
#	filename_hist = 'vic_TotalSoilMoist_%s_%s_%s_%s_WUSA_monthly_monmean.nc' % (model,modnum,"historical","1950_2005")
direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin
if (variable == "TotalSoilMoist"):
	filename_hist = '%s__%s.monmean.TotalSoilMoist.%s_%s_summer.nc' % (model,"historical","1950_2005",basin)
	filename = '%s__%s.monmean.TotalSoilMoist.%s_%s_summer.nc' % (model,scenario,years,basin)
else:
	filename_hist = '%s__%s.%s.%s.%s_%s_%s.nc' % (model,"historical",monthcalc,variable,"1950_2005",basin,season)
        filename = '%s__%s.%s.%s.%s_%s_%s.nc' % (model,scenario,monthcalc,variable,years,basin,season)

## load data
if (variable == "TotalSoilMoist"):
	lats,lons,sm_hist,datess_hist = unpack_netcdf_file_var(direc,filename_hist,"TotalSoilMoist")
	lats,lons,sm,datess = unpack_netcdf_file_var(direc,filename,"TotalSoilMoist") 
else:
	print(os.path.join(direc,filename_hist))
	print(os.path.join(direc,filename))
	lats,lons,sm_hist,datess_hist = unpack_netcdf_file_var(direc,filename_hist,variable)
        lats,lons,sm,datess = unpack_netcdf_file_var(direc,filename,variable)

## load historical mean SWE file and get mask
direc = '/raid9/gergel/agg_snowpack/goodleap/SWE'
filename = 'histmeanmask.nc' ## True where hist mean swe > 10 mm
filename_lowlands = 'histmeanmask_lowlands.nc' ## True where hist mean swe < 10 mm 
lats_swe,lons_swe,hist_swe,datess_swe = unpack_netcdf_file_var(direc,filename,"swe")
hist_swe_mod = create_mask_mtn_ranges(hist_swe,lats_swe,lons_swe)  
lats_swe,lons_swe,hist_noswe,datess_swe = unpack_netcdf_file_var(direc,filename_lowlands,"swe") 

####################################################################################################
## get lats and lons for pr and temp
lats_inc = list()
lons_inc = list()

## masking for lowlands 
if (basin == "nwinterior") or (basin == "missouri") or (basin == "coastalnorth") or (basin == "coastalsouth") or (basin == "lower_colorado") or (basin == "great_basin"):
	
	## number of months varies depending on winter vs. summer
	a,b,c = sm.shape
	print(a)
	print(b)
	print(c)
	if (season == "winter"):
		mos = 5
	else:
		mos = 3

	a,b,c = sm.shape
	sm_res = sm.reshape(mos,a/mos,b,c)
	sm_hist_res = sm_hist.reshape(mos,56,b,c) 

	if (variable == "pr"):
                sm_hist_res = sm_hist_res.sum(0)
                sm_res = sm_res.sum(0)
        else:
                sm_hist_res = sm_hist_res.mean(0)
                sm_res = sm_res.mean(0)

	if (basin == "coastalnorth"):
		#sm_swe_mask = np.ma.logical_and(hist_noswe,sm) ## mask with no swe mask  
		#sm_swe_mask_hist = np.ma.logical_and(hist_noswe,sm_hist) ## mask with no swe mask 

		#_masked = np.ma.masked_array(sm,mask=np.logical_not(sm_swe_mask)) 
		#sm_hist_masked = np.ma.masked_array(sm_hist,mask=np.logical_not(sm_swe_mask_hist))  

		## set zero values to -10000
		for i in np.arange(len(sm_res)):
			for j in np.arange(len(lats)):
				for k in np.arange(len(lons)):
					if hist_noswe[0,j,k] == 0 or sm_res.mask[i,j,k] == 1:
						sm_res[i,j,k] = -10000
					else:
						if i < 1:
							lats_inc.append(lats[j])
							lons_inc.append(lons[k]) 

		for i in np.arange(len(sm_hist_res)):
			for j in np.arange(len(lats)):
				for k in np.arange(len(lons)):
					if hist_noswe[0,j,k] == 0 or sm_hist_res.mask[i,j,k] == 1:
						sm_hist_res[i,j,k] = -10000

		## set -10000 values to be masked
		sm_final = np.ma.masked_equal(np.asarray(sm_res),-10000)
		sm_hist_final = np.ma.masked_equal(np.asarray(sm_hist_res),-10000) 

	### additional masking 
	if (basin == "nwinterior"):
		file = '/raid9/gergel/agg_snowpack/sm_summer/nwinterior.npz'
		data = np.load(file)
		basin_bool = data['nwinterior'] 
	elif (basin == "coastalsouth"):
		file = '/raid9/gergel/agg_snowpack/sm_summer/nwinterior.npz'
                data = np.load(file)
		basin_bool = data['cs']
	elif (basin == "missouri"):
		file = '/raid9/gergel/agg_snowpack/sm_summer/masks.npz'
		data = np.load(file)
		basin_bool = data['mo']
	elif (basin == "lower_colorado"):
		file = '/raid9/gergel/agg_snowpack/sm_summer/masks.npz'
		data = np.load(file)
		basin_bool = data['lc']
	elif (basin == "great_basin"):
		file = '/raid9/gergel/agg_snowpack/sm_summer/masks.npz'
		data = np.load(file)
		basin_bool = data['gb'] 
	
	## additional masking for everything but Coastal North
	if (basin != "coastalnorth"):
		## scenario mask 
		for i in np.arange(len(sm_res)):
			for j in np.arange(len(lats)):
				for k in np.arange(len(lons)):
					if basin_bool[j,k] == 0 or sm_res.mask[i,j,k] == 1 or hist_noswe[0,j,k] == 0 or lats[j] > 49:
						sm_res[i,j,k] = -10000
					else:
						if i < 1:
							lats_inc.append(lats[j])
							lons_inc.append(lons[k]) 

		for i in np.arange(len(sm_hist_res)):	
			for j in np.arange(len(lats)):
				for k in np.arange(len(lons)):
					if basin_bool[j,k] == 0 or sm_hist_res.mask[i,j,k] == 1 or hist_noswe[0,j,k] == 0 or lats[j] > 49:
						sm_hist_res[i,j,k] = -10000
		
		## finish masking
		sm_final = np.ma.masked_equal(np.asarray(sm_res),-10000)
		sm_hist_final = np.ma.masked_equal(np.asarray(sm_hist_res),-10000) 
## masking for uplands
else: 
	a,b,c = sm.shape	

	if (season == "winter"):
                mos = 5
        else:
                mos = 3

	sm_res = sm.reshape(mos,a/mos,b,c) 
	sm_hist_res = sm_hist.reshape(mos,56,b,c)

	if (variable == "pr"):
                sm_hist_res = sm_hist_res.sum(0)
                sm_res = sm_res.sum(0)
        else:
                sm_hist_res = sm_hist_res.mean(0)
                sm_res = sm_res.mean(0)

	## mask variable with > 10 mm historical mean SWE 

	for i in np.arange(len(sm_res)):
		for j in np.arange(len(lats)):
			for k in np.arange(len(lons)):
				if hist_swe_mod[0,j,k] == 0:
					sm_res[i,j,k] = -10000

	for i in np.arange(len(sm_hist_res)):
		for j in np.arange(len(lats)):
			for k in np.arange(len(lons)):
				if hist_swe_mod[0,j,k] == 0:
					sm_hist_res[i,j,k] = -10000

	sm_final = np.ma.masked_equal(np.asarray(sm_res),-10000) ## mask all values equal to -10000
	sm_hist_final = np.ma.masked_equal(np.asarray(sm_hist_res),-10000) ## mask all values equal to -10000 

	

#####################################################################################################
## processing masked data now
## subtract minimum historical soil moisture in each grid cell from each summer soil moisture average
sm_minstorage = sm_hist_final.min(0) ## calculate minimum historical soil moisture 
sm_in_storage = sm_final - sm_minstorage ## subtract minimum historical soil moisture from every point in time series for each grid cell 
'''
## get cell areas
latss,lonss = np.meshgrid(lats,lons,indexing='ij') 
vecfunc_create_gridcell_area_array = np.vectorize(create_gridcell_area_array) 
arr_for_areas = np.random.randn(len(lats),len(lons))
cellareas = create_gridcell_area_array(arr_for_areas,latss,lonss)
## multiply grid cells with cell areas
sm_minstor_area = np.ma.multiply(sm_in_storage,cellareas)*0.000001 ## also convert units
'''
## sum over grid cells
sm_sum = sm_in_storage.sum(axis=(1,2))*0.000001 ## convert soil moisture storage total to km 
sm_full = sm_in_storage ## keep sm in mm
sm_latslonss = sm_final.mean(0).compressed()
## for precip and temp analysis
if (variable == "pr") or (variable == "TotalSoilMoist") or (variable == "tasmin") or (variable == "tasmax"):
	if (scenario == "historical"):
		var = sm_final[19:-7,:,:].mean(0).compressed()
	else:
		var1 = sm_final[3:33,:,:].mean(0).compressed()
		var2 = sm_final[33:63,:,:].mean(0).compressed()
		var3 = sm_final[63:93,:,:].mean(0).compressed()
##### save arrays to files
if (type == "ensavg"):
	filearrayname = '/raid9/gergel/agg_snowpack/sm_summer/%s_%s.npz' %(basin,scenario)
else:
	if (variable == "pr") or (variable == "tasmin") or (variable == "tasmax"):
		filearrayname = '/raid9/gergel/agg_snowpack/climatology/arrays/%s_%s_%s_%s_%s.npz' %(variable,basin,model,scenario,season)
	else:
		filearrayname = '/raid9/gergel/agg_snowpack/sm_summer/%s_%s_%s.npz' %(basin,model,scenario)

if (variable == "TotalSoilMoist"):
	if (scenario == "historical"):
		np.savez(filearrayname,sm=np.asarray(sm_sum),sm_f=np.asarray(sm_full),var=var)
	else: 
		np.savez(filearrayname,sm=np.asarray(sm_sum),sm_f=np.asarray(sm_full),chunk1=var1,chunk2=var2,chunk3=var3)
else:
	if (scenario == "historical"):
		np.savez(filearrayname,var=var,lats=np.asarray(lats_inc),lons=np.asarray(lons_inc))
	else:
		np.savez(filearrayname,chunk1=var1,chunk2=var2,chunk3=var3,lats=np.asarray(lats_inc),lons=np.asarray(lons_inc))


if (type == "ensavg"):
	print("finished running script successfully for %s %s" %(basin,scenario))  
else:
	print("finished running script successfully for %s %s %s" %(basin,model,scenario))

		
