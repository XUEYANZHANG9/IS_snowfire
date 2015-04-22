#!/bin/python 
import math
import numpy as np 
from snowpack_functions import unpack_netcdf_gen,lat_lon_adjust,mask_latlon 
import sys

## get input args: basin, scenario
args = sys.argv[1:]
basin = args[0]
scenario = args[1]

## initialize arrays for swe, precip and temp
swe_april = list()
precip_tot = list()
temp_maximum = list()
temp_minimum = list()
temp_average = list()

## get data
lats, lons, swe, datess_swe = unpack_netcdf_gen("SWE", basin, scenario)
lats, lons, temp_max, datess_temp = unpack_netcdf_gen("tasmax", basin,scenario)
lats, lons, temp_min, datess_temp = unpack_netcdf_gen("tasmin", basin, scenario)
lats, lons, precip, datess_precip = unpack_netcdf_gen("pr", basin, scenario)

## adjust data for hydro years
precip = precip[3:-2,:,:]
swe = swe[1:,:,:]

## get historical SWE data to determine which lats/lons to include in analysis
lats, lons, swe_hist, datess_swe_hist = unpack_netcdf_gen("SWE", basin, "historical")

for i in np.arange(len(swe)): 	## loop over year
	for j in np.arange(len(lats)): 	## loop over latitude
		for k in np.arange(len(lons)):	### loop over longitude 
			### don't calculate area for missing value elements
			if (math.isnan(swe[i,j,k])) == False: 
				## REMOVE ADDITIONAL GRID CELLS ACCORDING TO LAT_LON_ADJUST FOR BOXES AND ADJUSTMENTS (LATER MASKS)
				if_in_box = mask_latlon(lats[j],lons[k],basin)
				adjust_mask = lat_lon_adjust(lats[j],lons[k],basin)
				if if_in_box and adjust_mask:
					historical_sum_swe = 0
					## CALCULATE MEAN HISTORICAL SWE	
					for year in np.arange(len(swe_hist)): 
						historical_sum_swe += swe_hist[year,j,k]
					mean_swe = historical_sum_swe/len(swe_hist)
					## EXCLUDE GRID CELLS WITH MEAN HISTORICAL SWE < 10 MM 
					if (mean_swe >= 10): 
						swe_april.append(swe[i,j,k])
						ind = i*5
						precip_total = precip[ind,j,k] + precip[ind+1,j,k] + precip[ind+2,j,k] +  precip[ind+3,j,k] + precip[ind+4,j,k]
						precip_tot.append(precip_total)
						temp_maxx = (temp_max[ind,j,k] + temp_max[ind+1,j,k] + temp_max[ind+2,j,k] + temp_max[ind+3,j,k] + temp_max[ind+4,j,k])/5
						temp_minn = (temp_min[ind,j,k] + temp_min[ind+1,j,k] + temp_min[ind+2,j,k] + temp_min[ind+3,j,k] + temp_min[ind+4,j,k])/5
						temp_maximum.append(temp_maxx) 
						temp_minimum.append(temp_minn)
						temp_average.append((temp_maxx + temp_minn)/2)
						

## save arrays to files for plotting in a different script
filearrayname = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/ensavg_%s_%s.npz' %(basin,scenario)
np.savez(filearrayname,swe=np.asarray(swe_april),precip=np.asarray(precip_tot),temp_max=np.asarray(temp_maximum),temp_min=np.asarray(temp_minimum),temp_avg=np.asarray(temp_average))
 


