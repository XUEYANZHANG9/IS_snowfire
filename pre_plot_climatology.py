
# In[104]:

from snowpack_functions import unpack_netcdf_file_var,lat_lon_adjust,mask_latlon,historical_sum_swe
import numpy as np
import os
import math 
import sys

args = sys.argv[1:]
variable = args[0]
chunk = args[1]
scenario = args[2]
basin = args[3]


## get data
direc = '/raid9/gergel/agg_snowpack/climatology/data/' 
filename = '%s_ensavg_%s_%s_%s.nc' %("pr",scenario,basin,chunk)
lats,lons,var,datess = unpack_netcdf_file_var(direc,filename,"pr")
filename = '%s_ensavg_%s_%s_%s.nc' %("tasmax",scenario,basin,chunk)
lats,lons,var_max,datess = unpack_netcdf_file_var(direc,filename,"air_temp_max")
filename = '%s_ensavg_%s_%s_%s.nc' %("tasmin",scenario,basin,chunk)
lats,lons,var_min,datess = unpack_netcdf_file_var(direc,filename,"air_temp_min")
var_series = list()
lats_inc = list()
lons_inc = list()
## process data 
        
for j in np.arange(len(lats)): ## loop over latitude
	for k in np.arange(len(lons)): ## loop over longitude
        	if (math.isnan(var[0,j,k])) == False: 
                	if_in_box = mask_latlon(lats[j],lons[k],basin)
                        adjust_mask = lat_lon_adjust(lats[j],lons[k],basin)
                        mean_swe = historical_sum_swe(j,k)
                        if if_in_box and adjust_mask and mean_swe: ## then use data and get average for each grid cell 
                            var_year = 0
			    length = 30
                            for i in np.arange(30): 
                                ind = i * 5 
                                if (variable == "pr"): 
                                    var_year += np.sum(np.asarray((var[ind:ind+5,j,k])))
                                else: 
                                    var_year += (np.mean(np.asarray(var_max[ind:ind+5,j,k])) + np.mean(np.asarray(var_min[ind:ind+5,j,k])))/2
                            if (variable == "pr"):
                                var_series.append((var_year/length))
                            else:
                                var_series.append((var_year/length)-273.15) ## append to array and convert from Kelvin to Celcius 
                            lats_inc.append(lats[j])
                            lons_inc.append(lons[k])
filearrayname = '/raid9/gergel/agg_snowpack/climatology/arrays/%s_%s_%s_%s.npz' %(variable,basin,scenario,chunk) 
np.savez(filearrayname,lats=np.asarray(lats_inc),lons=np.asarray(lons_inc),var=np.asarray(var_series)) 
print("saved array to %s" %filearrayname) 
