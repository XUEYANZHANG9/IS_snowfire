### USES ENSEMBLE AVERAGE OF 10 GCMS
### TAKES IN lats, lons, swe, gridcell elevations, basin, scenario
### spits out numpy array of lats, lons, elevation and grid cell total SWE  
def swe_elevation_mean(lats,lons,swe,datess,elev_corr_info,basin,scenario):
    import numpy as np
    import math 
    from snowpack_functions import unpack_netcdf_file_var,get_elev_for_lat_lon,mask_latlon,lat_lon_adjust
    
    ## get historical SWE for model so that historical mean can be determined for mask
    direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin
    file_hist = 'SWE_ensavg_%s_%s.nc' %("historical",basin)
    file = 'SWE_ensavg_%s_%s.nc' %(scenario,basin)
    lats_hist,lons_hist,swe_hist,datess_hist = unpack_netcdf_file_var(direc,file_hist,"swe")
    
    ## list for latitude and longitude values included in the historical mean mask 
    lats_lons_inc_in_mask = list()
    ## initialize lists for storing grid cell elevations
    if (scenario == "historical"):
    	swe_inc = list()
    	elev_inc = list()
    else:
	swe_1 = list()
	elev_1 = list()
	swe_2 = list()
	elev_2 = list()
	swe_3 = list()
	elev_3 = list()
    count = 0
    ################# loop through array and get latitude, longitude and swe values for each #############

    for j in np.arange(len(lats)):       ### loop over latitude
        for k in np.arange(len(lons)):   ### loop over longitude
            ### don't calculate area for missing value elements
            ### isnan will convert masked values to nan's, so this statement will evaluate to false if 
            ### the value exists (and thus is not masked)
            historical_mean_swe = 0
	    ## calculate historical mean SWE for grid cell
	    if (math.isnan(swe[0,j,k]) == False):
	    	if_in_box = mask_latlon(lats[j],lons[k],basin)
                adjust_mask = lat_lon_adjust(lats[j],lons[k],basin)
		if if_in_box and adjust_mask:
			historical_sum_swe = 0
            		for year in np.arange(len(swe_hist)):
                    		historical_sum_swe += swe_hist[year,j,k]
                	historical_mean_swe = historical_sum_swe/len(swe_hist)
	    	
            		if (historical_mean_swe >= 10): 
				count += 1
                		## get elevation of grid cell
                		elevation_individual_gridcell = get_elev_for_lat_lon(elev_corr_info,lats[j],lons[k])
                		## add swe and elevation values to lists depending on scenario
				if (scenario == "historical"):
					sum_swe = 0
					for year in np.arange(len(swe)): ## calculate mean swe
						sum_swe += swe[year,j,k]
					mean_swe = sum_swe/len(swe)
					mean_swe = mean_swe*0.001 # convert mm to meters
                			swe_inc.append(mean_swe)
                			elev_inc.append(elevation_individual_gridcell)
				else: 
					sum_swe = 0
					for year in np.arange(4,34):
						sum_swe += swe[year,j,k]
					mean_swe = sum_swe/len(np.arange(4,33))
					mean_swe = mean_swe*0.001 # convert mm to meters
					swe_1.append(mean_swe)
					elev_1.append(elevation_individual_gridcell)
					sum_swe = 0
					for year in np.arange(34,64):
                                        	sum_swe += swe[year,j,k]
                                        mean_swe = sum_swe/len(np.arange(4,33))
					mean_swe = mean_swe*0.001 # convert mm to meters
                        		swe_2.append(mean_swe)
                        		elev_2.append(elevation_individual_gridcell)
					sum_swe = 0
					for year in np.arange(64,94):
                                        	sum_swe += swe[year,j,k]
                                        mean_swe = sum_swe/len(np.arange(4,33))
					mean_swe = mean_swe*0.001 # convert mm to meters
                        		swe_3.append(mean_swe)
                        		elev_3.append(elevation_individual_gridcell)
    print(count)
    ##### save arrays to files for a multimodel average (and for spatial plots with lats and lons)
    ## define path based on scenario
    filearrayname = '/raid9/gergel/agg_snowpack/elevations/ensavg_%s_%s.npz' %(basin,scenario)
    if (scenario == "historical"):
    	np.savez(filearrayname,swe=np.asarray(swe_inc),elevations=np.asarray(elev_inc))
	return (swe_inc,elev_inc)
    else: 
	np.savez(filearrayname,swe1=np.asarray(swe_1),swe2=np.asarray(swe_2),swe3=np.asarray(swe_3),elev1=np.asarray(elev_1),elev2=np.asarray(elev_2),elev3=np.asarray(elev_3))
    	return (swe_1,swe_2,swe_3,elev_1,elev_2,elev_3)


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
if (scenario == "historical"):
	swe_inc, elev_inc = swe_elevation_mean(lats,lons,swe,datess,elev_corr_info,basin,scenario)
else:
	swe1,swe2,swe3,elev1,elev2,elev3 = swe_elevation_mean(lats,lons,swe,datess,elev_corr_info,basin,scenario)

##################### plot ############################
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import statsmodels.api as sm
plt.figure(figsize=(16,4))
lw=2.0
al=0.7
if (scenario == "historical"):
	plt.plot(swe_inc,elev_inc,'r.',alpha=al)
else: 
	plt.plot(swe1,elev1,'r.',alpha=al)
	plt.plot(swe2,elev2,'b.',alpha=al)
	plt.plot(swe3,elev3,'g.',alpha=al)
plt.xlabel('SWE [m]')
plt.ylabel('elevation [m]')
######## LOESS ########################
if (scenario == "historical"):
	loess = sm.nonparametric.lowess(elev_inc,swe_inc,frac=2./3)[:,1] ## possibly include frac value as well, i.e. frac= 1./3
	x_vals = np.linspace(np.min(np.asarray(swe_inc)),np.max(np.asarray(swe_inc)),num=len(np.asarray(elev_inc)))
	plt.plot(x_vals,loess,'b-',linewidth=lw)
else: ## split up signal into 30 year chunks 
	xvals = np.linspace(np.min(np.asarray(swe1)),np.max(np.asarray(swe1)),num=len(np.asarray(elev1)))
	loess1 = sm.nonparametric.lowess(elev1,swe1,frac=2./3)[:,1] ## possibly include frac value as well, i.e. frac= 1./3
	loess2 = sm.nonparametric.lowess(elev2,swe2,frac=2./3)[:,1] ## possibly include frac value as well, i.e. frac= 1./3
	loess3 = sm.nonparametric.lowess(elev3,swe3,frac=2./3)[:,1] ## possibly include frac value as well, i.e. frac= 1./3
	plt.plot(xvals,loess1,'r',linewidth=lw,label='2010-2039')
	plt.plot(xvals,loess2,'b',linewidth=lw,label='2040-2069')
	plt.plot(xvals,loess3,'g',linewidth=lw,label='2070-2099')
	plt.legend(loc='lower right')
plt.title('%s %s' %(scenario,basin)) 
## save plot 
direc = '/raid9/gergel/agg_snowpack/plots/'
model_spec = 'elevations'
plotname = 'SWE_ensavg_%s_%s_%s' % (model_spec,scenario, basin)
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath)


