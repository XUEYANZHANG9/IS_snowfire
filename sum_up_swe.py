### TAKES IN lats, lons, swe 
def sum_swe_mod(lats,lons,swe,basin,model,scenario):
    import numpy as np
    import math
    from snowpack_functions import lat_lon_adjust,get_dist,calc_area,unpack_netcdf_swe_month,mask_latlon
    resol=0.0625
    swe_yearly_agg = np.ndarray(shape = (len(swe),1), dtype=float)
    
    ## get historical SWE for model so that historical mean can be determined for mask
    lats_hist,lons_hist,swe_hist,datess_hist = unpack_netcdf_swe_month(basin,model,'historical')
    ## arrays for latitude and longitude values included in the historical mean mask 
    lats_lons_inc_in_mask = list()

    ################# loop through array and get latitude, longitude and swe values for each #############
    count_appending_latslons = 0

    for i in np.arange(len(swe)):     ### loop over year
    	count_appending_latslons += 1
        ## initialize value of SWE for each year to zero
        swe_gridcell_total = 0

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
                        		## calculate amount of swe in each grid cell: swe (in mm) * area of grid cell; adjust for units
                        		swe_gridcell = cellarea*(swe[i,j,k]*0.000001)
                        		## sum up swe
                        		swe_gridcell_total += swe_gridcell
					## ONLY ADD LATS/LONS TO LIST FOR FIRST LOOP
					if (count_appending_latslons < 2): 
                        			points = [lats[j],lons[k]]
                        			lats_lons_inc_in_mask.append(points)
                
        ## summed up yearly April 1 aggregate snowpack
        swe_yearly_agg[i] = swe_gridcell_total
    
    ##### save arrays to files for a multimodel average (and for spatial plots with lats and lons)
    ## define path based on scenario
    filearrayname = '/raid9/gergel/agg_snowpack/%s/%s_%s.npz' %(scenario,model,basin)
    np.savez(filearrayname,x=swe_yearly_agg)
    file_mask = '/raid9/gergel/agg_snowpack/%s/%s_latslonsinmask_%s.npz' %(scenario,basin,model)
    np.savez(file_mask,x=np.asarray(lats_lons_inc_in_mask))
    return (swe_yearly_agg,lats_lons_inc_in_mask)


# In[53]:

def aggregate_snowpack(basin,model,scenario):
    ####################      RUN SCRIPT       #######################
    from snowpack_functions import plot_swe,unpack_netcdf_swe_month
    lats,lons,swe,datess = unpack_netcdf_swe_month(basin, model, scenario)
    swe_yearly_agg,lats_lons_inc_in_mask = sum_swe_mod(lats,lons,swe,basin,model,scenario)
    plot_swe(datess,swe_yearly_agg,basin,model,scenario)
    print ("finished calculating aggregate snowpack for %s %s %s" %(basin,model,scenario))
    return (lats_lons_inc_in_mask)
    


# In[54]:
import sys

## get command line arguments
args = sys.argv[1:]
basin = args[0]
model = args[1]
scenario = args[2]
## call function
lats_lons_inc_in_mask = aggregate_snowpack(basin,model,scenario)
print ("finished calculating aggregate snowpack for %s %s %s" %(basin,model,scenario))
            
            


