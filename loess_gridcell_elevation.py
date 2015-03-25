### USES ENSEMBLE AVERAGE OF 10 GCMS
### TAKES IN lats, lons, swe, gridcell elevations, basin, scenario
### spits out numpy array of lats, lons, elevation and grid cell total SWE  
def swe_elevation_mean(lats,lons,swe,datess,elev_corr_info,basin,scenario):
    import numpy as np
    import math 
    from snowpack_functions import unpack_netcdf_file_var,get_elev_for_lat_lon
    
    ## get historical SWE for model so that historical mean can be determined for mask
    direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin
    file_hist = 'SWE_ensavg_%s_%s.nc' %("historical",basin)
    file = 'SWE_ensavg_%s_%s.nc' %(scenario,basin)
    lats_hist,lons_hist,swe_hist,datess_hist = unpack_netcdf_file_var(direc,file_hist,"swe")
    
    ## list for latitude and longitude values included in the historical mean mask 
    lats_lons_inc_in_mask = list()
    ## initialize lists for storing grid cell elevations
    swe_inc = list()
    elev_inc = list()
    
    ################# loop through array and get latitude, longitude and swe values for each #############

    for j in np.arange(len(lats)):       ### loop over latitude
        for k in np.arange(len(lons)):   ### loop over longitude
            ### don't calculate area for missing value elements
            ### isnan will convert masked values to nan's, so this statement will evaluate to false if 
            ### the value exists (and thus is not masked)
            historical_mean_swe = 0
	    ## calculate historical mean SWE for grid cell
            for year in np.arange(len(swe_hist)):
                historical_sum_swe = 0
                if (math.isnan(swe[year,j,k]) == False):
                    historical_sum_swe += swe_hist[year,j,k]
                    historical_mean_swe = historical_sum_swe/len(swe_hist)
	    # calculate mean SWE
            for year in np.arange(len(swe)):
                sum_swe = 0
                if (math.isnan(swe[year,j,k]) == False):
                    sum_swe += swe[year,j,k]
                    mean_swe = sum_swe/len(swe)
            if (historical_mean_swe > 10): 
                ## get elevation of grid cell
		mean_swe = mean_swe*0.001 # convert mm to meters
                elevation_individual_gridcell = get_elev_for_lat_lon(elev_corr_info,lats[j],lons[k])
                ## add swe and elevation values to lists
                swe_inc.append(mean_swe)
                elev_inc.append(elevation_individual_gridcell)
                    
    
    ##### save arrays to files for a multimodel average (and for spatial plots with lats and lons)
    ## define path based on scenario
    filearrayname = '/raid9/gergel/agg_snowpack/elevations/ensavg_%s_%s.npz' %(basin,scenario)
    np.savez(filearrayname,swe=np.asarray(swe_inc),elevations=np.asarray(elev_inc))
    return (swe_inc,elev_inc)


################################################ BEGIN LOESS ANALYSIS ######################################### 
import numpy as np
import sys
from snowpack_functions import unpack_netcdf_file_var, import_gridcell_elevation
## get command line arguments
args = sys.argv[1:]
basin = args[0]
scenario = args[1]
soil_file = '/raid9/gergel/agg_snowpack/soil_avail.txt'
elev_corr_info = import_gridcell_elevation(soil_file)
direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin
file = 'SWE_ensavg_%s_%s.nc' %(scenario,basin) 
lats, lons, swe, datess = unpack_netcdf_file_var(direc,file,"swe")
swe_inc, elev_inc = swe_elevation_mean(lats,lons,swe,datess,elev_corr_info,basin,scenario)

##################### plot ############################
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import statsmodels.api as sm
plt.figure(figsize=(16,4))
plt.xlabel('SWE in m')
plt.ylabel('elevation in m')
plt.plot(swe_inc,elev_inc,'r.')

######## LOESS ########################
loess = sm.nonparametric.lowess(elev_inc,swe_inc) ## possibly include frac value as well, i.e. frac= 1./3
x_vals = np.linspace(np.min(np.asarray(swe_inc)),np.max(np.asarray(swe_inc)),num=len(np.asarray(elev_inc)))
plt.plot(x_vals,loess,'b-')
## save plot 
direc = '/raid9/gergel/agg_snowpack/plots/'
model_spec = 'elevations'
plotname = 'SWE_ensavg_%s_%s_%s' % (model_spec,scenario, basin)
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath)


