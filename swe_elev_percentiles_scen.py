### TAKES IN lats, lons, swe 
### uses ensemble average over 10 gcms
def swe_percs(lats,lons,swe,datess, elev_corr_info, basin,scenario):
    import numpy as np
    import math
    from snowpack_functions import lat_lon_adjust,get_dist,calc_area,unpack_netcdf_swe_ensavg,mask_latlon,get_elev_for_lat_lon
    ## initialize lists for percentiles of elevations
    swe_10 = list()
    swe_25 = list()
    swe_50 = list()
    swe_75 = list()
    swe_90 = list()
    ## get historical SWE for model so that historical mean can be determined for mask
    lats_hist,lons_hist,swe_hist,datess_hist = unpack_netcdf_swe_ensavg(basin,'historical')

    for i in np.arange(len(swe)):     ### loop over year
	## start a new list of SWE and Elevation points every year
	swe_inc = list()
	elev_inc = list()
	## initialize SWE year total to zero
        swe_tot = 0

        for j in np.arange(len(lats)):       ### loop over latitude

            for k in np.arange(len(lons)):   ### loop over longitude
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
		    		########################### EXCLUDE GRID CELLS WITH MEAN HISTORICAL SWE < 10 MM 
                    		if (mean_swe >= 10): 
					# get swe and elevation values and add to list for each grid cell for the given year
					swe_inc.append(swe[i,j,k])
                        		elev_inc.append(get_elev_for_lat_lon(elev_corr_info,lats[j],lons[k]))
					## get total value of swe for given year
					swe_tot += swe[i,j,k]
        ## total value of swe for given year is swe_tot
        ## sort elev_inc by elevation and swe_inc in same way (ascending order)
	elev_sorted = sorted(elev_inc)
	swe_sorted = [swe_inc for (elev_inc,swe_inc) in sorted(zip(elev_inc,swe_inc))]	
	print("the length of swe_sorted is %f" %len(swe_sorted))
	## index lists for percentiles
	p10 = list()
	p25 = list()
	p50 = list()
	p75 = list()
	p90 = list()
	swe_cumsum = np.cumsum(swe_sorted)
	for num in np.arange(len(swe_cumsum)):
		if (swe_cumsum[num] >= 0.9*swe_tot):
			p90.append(num)
			print(num)
		elif (swe_cumsum[num] >= 0.75*swe_tot):
			p75.append(num)
			print("25 percent")
		elif (swe_cumsum[num] >= 0.5*swe_tot):
			p50.append(num)
		elif (swe_cumsum[num] >= 0.25*swe_tot):
			p25.append(num)
		elif (swe_cumsum[num] >= 0.1*swe_tot):
			p10.append(num)
		else:
			print("this swe sum is small")
	swe_10.append(elev_sorted[np.min(p10)])
	swe_25.append(elev_sorted[np.min(p25)])
	swe_50.append(elev_sorted[np.min(p50)])
	swe_75.append(elev_sorted[np.min(p75)])
	swe_90.append(elev_sorted[np.min(p90)]) 
    return (datess, swe_10,swe_25,swe_50,swe_75,swe_90)

### MOVING AVERAGE FUNCTION
def mv_avg(values,window):
	## this function takes in a vector and a number for the moving avg (i.e. if num = 10, then calculates 10-pt moving average)
	import numpy as np
	weights = np.repeat(1.0,window)/window
	sma = np.convolve(values,weights,'valid')
	return sma 

################################################ BEGIN ANALYSIS
import numpy as np
import sys
############################# import modified unpack_netcdf function
from snowpack_functions import unpack_netcdf_swe_ensavg, import_gridcell_elevation
import os

## get command line arguments
args = sys.argv[1:]
basin = args[0]
scenario = args[1]

soil_file = '/raid9/gergel/agg_snowpack/soil_avail.txt'
elev_corr_info = import_gridcell_elevation(soil_file)


lats, lons, swe, datess = unpack_netcdf_swe_ensavg(basin,scenario)
datess, swe_10,swe_25,swe_50,swe_75,swe_90 = swe_percs(lats,lons,swe,datess,elev_corr_info,basin,scenario)

e_10 = mv_avg(swe_10,10)
e_25 = mv_avg(swe_25,10)
e_50 = mv_avg(swe_50,10)
e_75 = mv_avg(swe_75,10)
e_90 = mv_avg(swe_90,10)
filearrayname = '/raid9/gergel/agg_snowpack/%s/percentiles_elev_ensavg_SWE_%s.npz' %(scenario,basin)
np.savez(filearrayname,e_10=np.asarray(e_10),e_25=np.asarray(e_25),e_50=np.asarray(e_50),e_75=np.asarray(e_75),e90=np.asarray(e_90))

  


