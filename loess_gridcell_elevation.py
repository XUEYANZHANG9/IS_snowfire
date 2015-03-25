### this function modifies swe_elevation_mean 
### USES ENSEMBLE AVERAGE OF 10 GCMS
### TAKES IN lats, lons, swe, gridcell elevations, basin, scenario
### spits out numpy array of lats, lons, elevation and grid cell total SWE  
def swe_elevation_mean(lats,lons,swe,datess,elev_corr_info,basin,model,scenario):
    import numpy as np
    import math 
    from snowpack_functions import unpack_netcdf,get_elev_for_lat_lon, calc_area, get_dist
    ### start calculating area of grid cells
    resol = 0.0625
    cellsize = 0.0625
    # radius_of_earth = 6371.228 # in km
    
    ## get historical SWE for model so that historical mean can be determined for mask
    scenario_for_mean = 'historical'
    lats_hist,lons_hist,swe_hist,datess_hist = unpack_netcdf(basin,model,scenario_for_mean)
    
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
    filearrayname = '/raid9/gergel/agg_snowpack/elevations/%s_%s_%s.npz' %(basin,model,scenario)
    np.savez(filearrayname,swe=np.asarray(swe_inc),elevations=np.asarray(elev_inc))
    return (swe_inc,elev_inc)


################################################ BEGIN ANALYSIS
import numpy as np
import sys
from snowpack_functions import unpack_netcdf, import_gridcell_elevation
# resol = 0.0625
# cellsize = 0.0625
# radius_of_earth = 6371.228 # in km
## get command line arguments
args = sys.argv[1:]
basin = args[0]
model = args[1]
scenario = args[2]
soil_file = '/raid9/gergel/agg_snowpack/soil_avail.txt'
elev_corr_info = import_gridcell_elevation(soil_file)
lats, lons, swe, datess = unpack_netcdf(basin,model,scenario)
swe_inc, elev_inc = swe_elevation_mean(lats,lons,swe,datess,elev_corr_info,basin,model,scenario)

# In[7]:
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
plt.ion()
# get_ipython().magic(u'matplotlib inline')
plt.figure(figsize=(16,4))
plt.grid()
plt.xlabel('SWE in m')
plt.ylabel('elevation in m')
plt.plot(elev_inc,swe_inc,'.')

import numpy as np
### do quick linear regression to add a trendline
coeffs = np.polyfit(elev_inc,swe_inc,1)
polynomial = np.poly1d(coeffs)
ys = polynomial(elev_inc)

### add trendline
plt.plot(elev_inc,ys,'m')
plt.title('Average elevation vs mean SWE of gridcell: %s  %s  %s %s' %(scenario,basin,model,polynomial))

## save plot 
direc = '/raid9/gergel/agg_snowpack/plots/'
model_spec = 'elevations'
plotname = 'SWE_%s_%s_%s_%s' % (model_spec,scenario, model, basin)
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath)


