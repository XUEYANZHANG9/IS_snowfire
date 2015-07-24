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
	print(arr.shape) 
	return(vecfunc_calc_area(lats,lons,resol)) 
def create_mask_mtn_ranges(arr,lats_mesh,lons_mesh):
	import numpy as np
	import math
	from snowpack_functions import mask_out_other_mtns
	if (math.isnan(arr) == False): 
		res = mask_out_other_mtns(lats_mesh,lons_mesh)
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

	a,b,c = sm_masked.shape
	
	## mask further with lats/lons 
	gg, la_hist, lo_hist = np.meshgrid(np.arange(len(sm_hist_masked)),lats,lons,indexing='ij')  
	
	gg,la,lo = np.meshgrid(np.arange(len(sm_masked)),lats,lons,indexing='ij') 
	
	vecfunc_create_mask_mtn_ranges = np.vectorize(create_mask_mtn_ranges)
	
	sm_hist_final = vecfunc_create_mask_mtn_ranges(sm_hist_masked,la_hist,lo_hist)
	sm_final = vecfunc_create_mask_mtn_ranges(sm_masked,la,lo)  
	

#####################################################################################################
## subtract minimum historical soil moisture in each grid cell from each summer soil moisture average
sm_minstorage = np.ma.apply_along_axis(np.min,0,sm_hist_final) ## calculate minimum historical soil moisture 
sm_in_storage = sm_final - sm_minstorage ## subtract minimum historical soil moisture from every point in time series for each grid cell 
## get cell areas
latss,lonss = np.meshgrid(lats,lons,indexing='ij') 
vecfunc_create_gridcell_area_array = np.vectorize(create_gridcell_area_array) 
arr_for_areas = np.random.randn(len(lats),len(lons))
cellareas = create_gridcell_area_array(arr_for_areas,latss,lonss)
## multiply grid cells with cell areas
sm_minstor_area = np.ma.multiply(sm_minstorage,cellareas)*0.000001 ## also convert units
## sum over grid cells
sm_sum = np.ma.apply_over_axes(np.sum,sm_minstor_area,[1,2])



		
