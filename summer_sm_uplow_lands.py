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

def create_gridcell_area_array(no_years,lats,lons):
	cellareas = np.ndarray(shape = (no_years,len(lats),len(lons)),dtype=float)
	resol = 0.0625 ## 1/16th degree resolution
	import numpy as np
	from snowpack_functions import calc_area
	for i in np.arange(no_years):
		for j in len(lats):
			for k in len(lons):
				cellareas[i,j,k] = calc_area(lats[j],lons[k],resol) 
	return(cellareas) 
def create_mask_mtn_ranges(arr,j,k,lats,lons):
	import numpy as np
	import math
	from snowpack_functions import mask_out_other_mtns
	if (math.isnan(arr) == False): 
		res = mask_out_other_mtns(lats[j],lons[k])
		if (res == False):
			return(np.nan)
		else:
			return(arr) 
	else: 
		return(arr) 
## get input arguments 
args=sys.argv[1:]
basin = args[1] 
scenario = args[2] 

## import data 
direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin 
filename_hist = 'TotalSoilMoist_ensavg_%s_%s_summer.nc' %("historical",basin)
filename = 'TotalSoilMoist_ensavg_%s_%s_summer.nc' %(scenario,basin)


## load data
lats,lons,sm_hist,datess_hist = unpack_netcdf_file_var(direc,filename_hist,"TotalSoilMoist")
lats,lons,sm,datess = unpack_netcdf_file_var(direc,filename,"TotalSoilMoist") 

## load historical mean SWE file and get mask
direc = '/raid9/gergel/agg_snowpack/goodleap/SWE'
filename = 'histmeanmask.nc' ## True where hist mean swe > 10 mm
filename_lowlands = 'histmeanmask_lowlands.nc' ## True where hist mean swe < 10 mm 
lats_swe,lons_swe,hist_swe,datess_swe = unpack_netcdf_file_var(direc,filename,"swe") 
lats_swe,lons_swe,hist_noswe,datess_swe = unpack_netcdf_file_var(direc,filename_lowlands,"swe") 

####################################################################################################
## masking for lowlands 
if (basin == "nwinterior") or (basin == "plains") or (basin == "coastalnorth") or (basin == "coastalsouth") or (basin == "southwest"):
	sm_swe_mask = np.ma.logical_and(hist_noswe,sm) ## mask with no swe mask  
	
	sm_masked = np.ma.masked_array(sm,mask=sm_swe_mask) 
	sm_hist_masked = np.ma.masked_array(sm_hist,mask=sm_swe_mask) 
	
	a,b,c = sm_masked.shape
	
	sm_masked_res = sm_masked.reshape(3,a/3,b,c) 
	sm_hist_masked_res = sm_hist_masked.reshape(3,56,b,c) 
	
	sm_hist_final = np.ma.apply_along_axis(np.mean,0,sm_hist_masked_res) 
	sm_final = np.ma.apply_along_axis(np.mean,0,sm_masked_res)
	
## masking for uplands
else: 
	## mask sm with > 10 mm historical mean SWE
	sm_swe_mask = np.ma.logical_and(hist_swe,sm) ## mask with swe mask 
	
	sm_masked = np.ma.masked_array(sm,mask=sm_swe_mask) 
	sm_hist_masked = np.ma.masked_array(sm_hist,mask=sm_swe_mask) 	

	## mask further with lats/lons 
	i, j, k = np.meshgrid(*map(np.arange,sm_masked.shape),indexing='ij')
	# sm_hist_final = np.ma.apply_over_axes(create_mask_mtn_ranges,sm_masked,j,k,lats,lons,[1,2]) 
	vecfunc_create_mask_mtn_ranges = np.vectorize(create_mask_mtn_ranges)
	sm_hist_final = vecfunc_create_mask_mtn_ranges(sm_hist_masked,j,k,lats,lons) 
	# sm_final = np.ma.apply_over_axes(create_mask_mtn_ranges,sm_hist_masked,j,k,lats,lons,[1,2])

#####################################################################################################
## subtract minimum historical soil moisture in each grid cell from each summer soil moisture average
sm_minstorage = np.ma.apply_along_axis(subtract_min_sm,0,sm_final,sm_hist_final)
## get cell areas
cellareas = create_gridcell_area_array(a,lats,lons)
## multiply grid cells with cell areas
sm_minstor_area = np.ma.multiply(sm_minstorage,cellareas)*0.000001 ## also convert units
## sum over grid cells
sm_sum = np.ma.apply_over_axes(np.sum,sm_minstor_area,[1,2])



		
