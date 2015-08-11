#!/bin/python 
import math
import numpy as np 
from snowpack_functions import unpack_netcdf_gen,lat_lon_adjust,mask_latlon,unpack_netcdf_file_var,historical_sum_swe,mask_out_other_mtns
import sys

## get input args: basin, scenario
args = sys.argv[1:]
type = args[0] 
basin = args[1]
if (type == "ensavg"):
	scenario = args[2]
else:
	model = args[2]
	scenario = args[3]

## initialize arrays for swe, precip and temp
if (scenario == "historical"):
	swe_april = list()
	precip_tot = list()
	temp_average = list()
else:
	swe_april_2010_2039 = list()
	swe_april_2040_2069 = list()
	swe_april_2070_2099 = list()
	precip_tot_2010_2039 = list()
        precip_tot_2040_2069 = list()
        precip_tot_2070_2099 = list()
	temp_average_2010_2039 = list()
        temp_average_2040_2069 = list()
        temp_average_2070_2099 = list()

lats_inc = list()
lons_inc = list()
## get data

direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin

if (type == "ensavg"):
        file_swe = 'SWE_ensavg_%s_%s.nc' %(scenario,basin)
	file_tasmax = 'tasmax_ensavg_%s_%s.nc' %(scenario,basin)
	file_tasmin = 'tasmin_ensavg_%s_%s.nc' %(scenario,basin)
	file_pr = 'pr_ensavg_%s_%s.nc' %(scenario,basin)
else:
        if (scenario == "historical"):
                file_swe = '%s__%s.monday1.SWE.1950_2005_%s.nc' %(model,scenario,basin)
        	file_tasmax = '%s__%s.monmean.tasmax.1950_2005_%s.nc' %(model,scenario,basin)
		file_tasmin = '%s__%s.monmean.tasmin.1950_2005_%s.nc' %(model,scenario,basin)
		file_pr = '%s__%s.monsum.pr.1950_2005_%s.nc' %(model,scenario,basin)
	else:
                file_swe = '%s__%s.monday1.SWE.2006_2099_%s.nc' %(model,scenario,basin)
		file_tasmax = '%s__%s.monmean.tasmax.2006_2099_%s.nc' %(model,scenario,basin)
		file_tasmin = '%s__%s.monmean.tasmin.2006_2099_%s.nc' %(model,scenario,basin)		
		file_pr = '%s__%s.monsum.pr.2006_2099_%s.nc' %(model,scenario,basin)
print(direc)
print(file_swe) 
lats, lons, swe, datess_swe = unpack_netcdf_file_var(direc,file_swe,"swe")
lats, lons, temp_max, datess_temp = unpack_netcdf_file_var(direc,file_tasmax,"air_temp_max")
lats, lons, temp_min, datess_temp = unpack_netcdf_file_var(direc,file_tasmin,"air_temp_min")
lats, lons, precip, datess_precip = unpack_netcdf_file_var(direc,file_pr,"pr")

## adjust data for hydro years
precip = precip[3:-2,:,:]
swe = swe[1:,:,:]
temp_max = temp_max[3:-2,:,:]
temp_min = temp_min[3:-2,:,:]
datess_swe = datess_swe[1:]
datess_precip = datess_precip[3:-2]

## get historical SWE data to determine which lats/lons to include in analysis
lats, lons, swe_hist, datess_swe_hist = unpack_netcdf_gen("SWE", basin, "historical")

for j in np.arange(len(lats)): 	## loop over latitude
	for k in np.arange(len(lons)): 	## loop over longitude
		### don't calculate area for missing value elements
		if (math.isnan(swe[0,j,k])) == False: 
			## REMOVE ADDITIONAL GRID CELLS ACCORDING TO LAT_LON_ADJUST FOR BOXES AND ADJUSTMENTS (LATER MASKS)
			#if_in_box = mask_latlon(lats[j],lons[k],basin)
			#adjust_mask = lat_lon_adjust(lats[j],lons[k],basin)
			if_in_box = mask_out_other_mtns(lats[j],lons[k]) 
			if if_in_box:
				mean_swe = historical_sum_swe(j,k) 
				'''
				historical_sum_swe = 0
				## CALCULATE MEAN HISTORICAL SWE	
				for year in np.arange(len(swe_hist)): 
					historical_sum_swe += swe_hist[year,j,k]
				mean_swe = historical_sum_swe/len(swe_hist)
				## EXCLUDE GRID CELLS WITH MEAN HISTORICAL SWE < 10 MM 
				'''
				if (mean_swe): ## if historical mean swe of this grid cell is > 10 mm, include it for analysis, otherwise don't 
					swe_avg = 0
					temp_avg = 0
					swe_avg1 = 0
					temp_avg1 = 0
					swe_avg2 = 0
                                	temp_avg2 = 0
					swe_avg3 = 0
                                	temp_avg3 = 0
					for i in np.arange(len(swe)): 
						ind = i*5
						tempmax = (temp_max[ind,j,k] + temp_max[ind+1,j,k] + temp_max[ind+2,j,k] + temp_max[ind+3,j,k] + temp_max[ind+4,j,k])/5
                                        	tempmin = (temp_min[ind,j,k] + temp_min[ind+1,j,k] + temp_min[ind+2,j,k] + temp_min[ind+3,j,k] + temp_min[ind+4,j,k])/5
						tempavg = (tempmax + tempmin)/2
						swee = swe[i,j,k]
						
						if (scenario == "historical"):
							swe_avg += swee
							temp_avg += tempavg
						else:
							if datess_swe[i].year >= 2010 and datess_swe[i].year <= 2039:
								swe_avg1 += swee
								temp_avg1 += tempavg
							elif datess_swe[i].year >= 2040 and datess_swe[i].year <= 2069:
								swe_avg2 += swee
                                                                temp_avg2 += tempavg
							elif datess_swe[i].year >= 2070 and datess_swe[i].year <= 2099:
								swe_avg3 += swee
                                                                temp_avg3 += tempavg
					if (scenario == "historical"):
						swe_april.append(swe_avg/len(swe))
						temp_average.append(temp_avg/len(swe)) 
					else: 			
						swe_april_2010_2039.append(swe_avg1/30) 
						temp_average_2010_2039.append(temp_avg1/30)
						swe_april_2040_2069.append(swe_avg2/30)
                                        	temp_average_2040_2069.append(temp_avg2/30)
						swe_april_2070_2099.append(swe_avg3/30)
                                        	temp_average_2070_2099.append(temp_avg3/30)
						
					lats_inc.append(lats[j])
					lons_inc.append(lons[k]) 
## save arrays to files for plotting in a different script
if (type == "ensavg"):
	filearrayname = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/ensavg_%s_%s.npz' %(basin,scenario)
else:
	filearrayname = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/%s_%s_%s.npz' %(model,basin,scenario)
if (scenario == "historical"):
	np.savez(filearrayname,swe=np.asarray(swe_april),precip=np.asarray(precip_tot),temp_avg=np.asarray(temp_average),lats=np.asarray(lats_inc),lons=np.asarray(lons_inc))
else:
	np.savez(filearrayname,swe_2010_2039=np.asarray(swe_april_2010_2039),swe_2040_2069=np.asarray(swe_april_2040_2069),swe_2070_2099=np.asarray(swe_april_2070_2099),
		precip_2010_2039=np.asarray(precip_tot_2010_2039),precip_2040_2069=np.asarray(precip_tot_2040_2069),precip_2070_2099=np.asarray(precip_tot_2070_2099),
		temp_avg_2010_2039=np.asarray(temp_average_2010_2039),temp_avg_2040_2069=np.asarray(temp_average_2040_2069),temp_avg_2070_2099=np.asarray(temp_average_2070_2099),
		lats=np.asarray(lats_inc),lons=np.asarray(lons_inc))
print("saved array to %s" %filearrayname) 
