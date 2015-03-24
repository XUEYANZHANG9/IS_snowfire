### TAKES IN lats, lons, swe 
def sum_swe_mod(lats,lons,swe,basin,scenario):
    import numpy as np
    import math
    from snowpack_functions import lat_lon_adjust,get_dist,calc_area,unpack_netcdf_swe_month,mask_latlon,unpack_netcdf_file_var
    resol=0.0625
    swe_yearly_agg = np.ndarray(shape = (len(swe),1), dtype=float)
    sm_yearly_agg_mar = np.ndarray(shape = (len(swe),1),dtype=float)
    sm_yearly_agg_aug = np.ndarray(shape = (len(swe),1),dtype=float)
    
    ## get historical SWE for model so that historical mean can be determined for mask
    direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin 
    file_swe = 'SWE_ensavg_%s_%s.nc' %(scenario,basin)
    file_swe_hist = 'SWE_ensavg_%s_%s.nc' %("historical",basin)
    file_sm_mar = 'TotalSoilMoist_ensavg_%s_%s_march.nc' %(scenario,basin)
    file_sm_aug = 'TotalSoilMoist_ensavg_%s_%s_august.nc' %(scenario,basin)
    lats_hist,lons_hist,swe_hist,datess_hist = unpack_netcdf_file_var(direc,file_swe_hist,"swe")
    lats,lons,swe,datess_swe = unpack_netcdf_file_var(direc,file_swe,"swe")
    lats,lons,sm_mar,datess_sm_mar = unpack_netcdf_file_var(direc,file_sm_mar,"TotalSoilMoist")
    lats,lons,sm_aug,datess_sm_aug = unpack_netcdf_file_var(direc,file_sm_aug,"TotalSoilMoist")
    ## arrays for latitude and longitude values included in the historical mean mask 
    lats_lons_inc_in_mask = list()

    ################# loop through array and get latitude, longitude and swe values for each #############
    count_appending_latslons = 0

    for i in np.arange(len(swe)):     ### loop over year
    	count_appending_latslons += 1
        ## initialize value of SWE for each year to zero
        swe_gridcell_total = 0
	sm_mar_gridcell_total = 0
	sm_aug_gridcell_total = 0

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
					### calculate area of grid cell
                        		cellarea = calc_area(lats[j],lons[k],resol)
                        		## calculate amount of swe and soil moisture in each grid cell: swe (in mm) * area of grid cell; adjust for units
                        		swe_gridcell = cellarea*(swe[i,j,k]*0.000001)
					sm_mar_gridcell = cellarea*(sm_mar[i,j,k]*0.000001)
					sm_aug_gridcell = cellarea*(sm_aug[i,j,k]*0.000001)
                        		## sum up swe and soil moisture
                        		swe_gridcell_total += swe_gridcell
					sm_mar_gridcell_total += sm_mar_gridcell 
					sm_aug_gridcell_total += sm_aug_gridcell
					## ONLY ADD LATS/LONS TO LIST FOR FIRST LOOP
					if (count_appending_latslons < 2): 
                        			points = [lats[j],lons[k]]
                        			lats_lons_inc_in_mask.append(points)
                
        ## summed up yearly April 1 aggregate snowpack
        swe_yearly_agg[i] = swe_gridcell_total
	sm_yearly_agg_mar[i] = sm_mar_gridcell_total
	sm_yearly_agg_aug[i] = sm_aug_gridcell_total
    
    ##### save arrays to files for a multimodel average (and for spatial plots with lats and lons)
    ## define path based on scenario
    filearrayname = '/raid9/gergel/agg_snowpack/%s/%s.npz' %(scenario,basin)
    np.savez(filearrayname,dates=datess_swe,swe=swe_yearly_agg,sm_mar=sm_yearly_agg_mar,sm_aug=sm_yearly_agg_aug,latslons=np.asarray(lats_lons_inc_in_mask))
    #file_mask = '/raid9/gergel/agg_snowpack/%s/%s_latslonsinmask_%s.npz' %(scenario,basin,model)
    #np.savez(file_mask,x=np.asarray(lats_lons_inc_in_mask))




from snowpack_functions import unpack_netcdf_file_var
import sys
## get command line arguments
args = sys.argv[1:]
basin = args[0]
scenario = args[1]
direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin
file_swe = 'SWE_ensavg_%s_%s.nc' %(scenario,basin)
lats,lons,swe,datess = unpack_netcdf_file_var(direc,file_swe,"swe")
sum_swe_mod(lats,lons,swe,basin,scenario)

print ("finished calculating aggregate snowpack and soil moisture for %s %s" %(basin,scenario))
            
            


