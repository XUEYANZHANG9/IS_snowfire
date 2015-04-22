#!/bin/python 
import math
import numpy as np 
from snowpack_functions import unpack_netcdf_gen,lat_lon_adjust,mask_latlon 
import sys

## get input args: basin, scenario
args = sys.argv[1:]
basin = args[0]

## initialize arrays for swe, precip and temp
swe_april = list()
precip_tot = list()
temp_average = list()
rd_lats = list()
rd_lons = list()
tr_lats = list()
tr_lons = list()
sd_lats = list()
sd_lons = list()

## get historical data
lats, lons, swe, datess_swe = unpack_netcdf_gen("SWE", basin, "historical")
lats, lons, temp_max, datess_temp = unpack_netcdf_gen("tasmax", basin,"historical")
lats, lons, temp_min, datess_temp = unpack_netcdf_gen("tasmin", basin, "historical")
lats, lons, precip, datess_precip = unpack_netcdf_gen("pr", basin, "historical")

## adjust data for hydro years
precip = precip[3:-2,:,:]
swe = swe[1:,:,:]
temp_max = temp_max[3:-2,:,:]
temp_min = temp_min[3:-2,:,:]
datess_swe = datess_swe[1:]
datess_precip = datess_precip[3:-2]

## get historical SWE data to determine which lats/lons to include in analysis
lats, lons, swe_hist, datess_swe_hist = unpack_netcdf_gen("SWE", basin, "historical")

## get RD, SD, TR historical classifications
for j in np.arange(len(lats)): 	## loop over latitude
	for k in np.arange(len(lons)): 	## loop over longitude
		for i in np.arange(len(swe)):	### loop over year
			## array for temp average
			temp_averrage = list()
			
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
						ind = i*5
						temp_maxx = (temp_max[ind,j,k] + temp_max[ind+1,j,k] + temp_max[ind+2,j,k] + temp_max[ind+3,j,k] + temp_max[ind+4,j,k])/5
                                                temp_minn = (temp_min[ind,j,k] + temp_min[ind+1,j,k] + temp_min[ind+2,j,k] + temp_min[ind+3,j,k] + temp_min[ind+4,j,k])/5
						temp_averrage.append((temp_maxx + temp_minn)/2)
		## if length of temp_averrage list is > 0, then the grid cell should be included, then classify it
		if len(temp_averrage) > 0:
			if np.mean(temp_averrage) >= 278.15: 
				rd_lats.append(j)
				rd_lons.append(k)
			elif np.mean(temp_averrage) > 267.15 and np.mean(temp_averrage) < 278.15:
				tr_lats.append(j)
				tr_lons.append(k)
			elif np.mean(temp_averrage) <= 267.15:
				sd_lats.append(j)
				sd_lons.append(k)

## classifications established. now get data for each of them for historical and then future scenarios 
def get_rd_tr_sd_precip_swe(scen,lats,lons,swe,precip):
	## swe and precip are already adjusted for hydro years 
	## this works for historical,rcp4.5 and rcp8.5 scenarios
	## also works for RD,TR,SD
	scenario = scen 
	precip_class = list()
	swe_class = list()
	swe_2010_2039 = list()
        precip_2010_2039 = list()
        swe_2040_2069 = list()
        precip_2040_2069 = list()
        swe_2070_2099 = list()
        precip_2070_2099 = list()
	if (len(lats) == 0):
		if (scenario == "historical"):
			return(np.asarray(swe_class).flatten(),np.asarray(precip_class).flatten())
		else:
			return(np.asarray(swe_2010_2039).flatten(),np.asarray(precip_2010_2039).flatten(),np.asarray(swe_2040_2069).flatten(),np.asarray(precip_2040_2069).flatten(),np.asarray(swe_2070_2099).flatten(),np.asarray(precip_2070_2099).flatten())
	else: 
		for gridcell in np.arange(len(lats)):
                        swe_class_part = swe[:,lats[gridcell],lons[gridcell]]
                        precip_gridcell = precip[:,lats[gridcell],lons[gridcell]]
                        precip_gridcell_reshape = precip_gridcell.reshape(5,len(swe))
                        precip_sum = np.sum(precip_gridcell_reshape,axis=0)
                        precip_class.append(precip_sum)
			swe_class.append(swe_class_part)
		if (scenario == "historical"):
                	return(np.asarray(swe_class).flatten(),np.asarray(precip_class).flatten())
		else:
			swe_class = np.asarray(swe_class)
			precip_class = np.asarray(precip_class)
			for x in range(3,33):
				swe_2010_2039.append(swe_class[:,x])
				precip_2010_2039.append(precip_class[:,x])
			for x in range(33,63):
				swe_2040_2069.append(swe_class[:,x])
				precip_2040_2069.append(precip_class[:,x])
			for x in range(63,93):
				swe_2070_2099.append(swe_class[:,x])
				precip_2070_2099.append(precip_class[:,x])
			return(np.asarray(swe_2010_2039).flatten(),np.asarray(precip_2010_2039).flatten(),np.asarray(swe_2040_2069).flatten(),np.asarray(precip_2040_2069).flatten(),np.asarray(swe_2070_2099).flatten(),np.asarray(precip_2070_2099).flatten())
## get historical rd,tr,sd
swe_hist_rd,precip_hist_rd = get_rd_tr_sd_precip_swe("historical",rd_lats,rd_lons,swe,precip)
swe_hist_tr,precip_hist_tr = get_rd_tr_sd_precip_swe("historical",tr_lats,tr_lons,swe,precip)
swe_hist_sd,precip_hist_sd = get_rd_tr_sd_precip_swe("historical",sd_lats,sd_lons,swe,precip)

## get rcp4.5 data
lats, lons, swe_rcp45, datess_swe = unpack_netcdf_gen("SWE", basin, "rcp45")
lats, lons, precip_rcp45, datess_precip = unpack_netcdf_gen("pr", basin, "rcp45")
precip_rcp45 = precip_rcp45[3:-2,:,:]
swe_rcp45 = swe_rcp45[1:,:,:]	

## get rcp45 rd,tr,sd
swe_rcp45_2010_2039_rd,swe_rcp45_2040_2069_rd,swe_rcp45_2070_2099_rd,precip_rcp45_2010_2039_rd,precip_rcp45_2040_2069_rd,precip_rcp45_2070_2099_rd = get_rd_tr_sd_precip_swe("rcp45",rd_lats,rd_lons,swe_rcp45,precip_rcp45)
swe_rcp45_2010_2039_tr,swe_rcp45_2040_2069_tr,swe_rcp45_2070_2099_tr,precip_rcp45_2010_2039_tr,precip_rcp45_2040_2069_tr,precip_rcp45_2070_2099_tr = get_rd_tr_sd_precip_swe("rcp45",tr_lats,tr_lons,swe_rcp45,precip_rcp45)
swe_rcp45_2010_2039_sd,swe_rcp45_2040_2069_sd,swe_rcp45_2070_2099_sd,precip_rcp45_2010_2039_sd,precip_rcp45_2040_2069_sd,precip_rcp45_2070_2099_sd = get_rd_tr_sd_precip_swe("rcp45",sd_lats,sd_lons,swe_rcp45,precip_rcp45)

## get rcp8.5 data
lats, lons, swe_rcp85, datess_swe = unpack_netcdf_gen("SWE", basin, "rcp85")
lats, lons, precip_rcp85, datess_precip = unpack_netcdf_gen("pr", basin, "rcp85")
precip_rcp85 = precip_rcp85[3:-2,:,:]
swe_rcp85 = swe_rcp85[1:,:,:]

	
## get rcp85 rd, tr, sd
swe_rcp85_2010_2039_rd,swe_rcp85_2040_2069_rd,swe_rcp85_2070_2099_rd,precip_rcp85_2010_2039_rd,precip_rcp85_2040_2069_rd,precip_rcp85_2070_2099_rd = get_rd_tr_sd_precip_swe("rcp85",rd_lats,rd_lons,swe_rcp85,precip_rcp85)
swe_rcp85_2010_2039_tr,swe_rcp85_2040_2069_tr,swe_rcp85_2070_2099_tr,precip_rcp85_2010_2039_tr,precip_rcp85_2040_2069_tr,precip_rcp85_2070_2099_tr = get_rd_tr_sd_precip_swe("rcp85",tr_lats,tr_lons,swe_rcp85,precip_rcp85)
swe_rcp85_2010_2039_sd,swe_rcp85_2040_2069_sd,swe_rcp85_2070_2099_sd,precip_rcp85_2010_2039_sd,precip_rcp85_2040_2069_sd,precip_rcp85_2070_2099_sd = get_rd_tr_sd_precip_swe("rcp85",sd_lats,sd_lons,swe_rcp85,precip_rcp85)


## save arrays to files for plotting in a different script
filearrayname = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/constantclass_ensavg_%s_hist.npz' %(basin)
filearrayname2 = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/constantclass_ensavg_%s.npz' %(basin)
np.savez(filearrayname,swe_rd=np.asarray(swe_hist_rd),precip_rd=np.asarray(precip_hist_rd),swe_tr=np.asarray(swe_hist_tr),precip_tr=np.asarray(precip_hist_tr), swe_sd=np.asarray(swe_hist_sd),precip_sd=np.asarray(precip_hist_sd))
np.savez(filearrayname2,
	swe_rcp45_2010_2039_rd=np.asarray(swe_rcp45_2010_2039_rd),swe_rcp45_2040_2069_rd=np.asarray(swe_rcp45_2040_2069_rd),swe_rcp45_2070_2099_rd=np.asarray(swe_rcp45_2070_2099_rd),
	swe_rcp45_2010_2039_tr=np.asarray(swe_rcp45_2010_2039_tr),swe_rcp45_2040_2069_tr=np.asarray(swe_rcp45_2040_2069_tr),swe_rcp45_2070_2099_tr=np.asarray(swe_rcp45_2070_2099_tr),
	swe_rcp45_2010_2039_sd=np.asarray(swe_rcp45_2010_2039_sd),swe_rcp45_2040_2069_sd=np.asarray(swe_rcp45_2040_2069_sd),swe_rcp45_2070_2099_sd=np.asarray(swe_rcp45_2070_2099_sd),
	precip_rcp45_2010_2039_rd=np.asarray(precip_rcp45_2010_2039_rd),precip_rcp45_2040_2069_rd=np.asarray(precip_rcp45_2040_2069_rd),precip_rcp45_2070_2099_rd=np.asarray(precip_rcp45_2070_2099_rd),
	precip_rcp45_2010_2039_tr=np.asarray(precip_rcp45_2010_2039_tr),precip_rcp45_2040_2069_tr=np.asarray(precip_rcp45_2040_2069_tr),precip_rcp45_2070_2099_tr=np.asarray(precip_rcp45_2070_2099_tr),
	precip_rcp45_2010_2039_sd=np.asarray(precip_rcp45_2010_2039_sd),precip_rcp45_2040_2069_sd=np.asarray(precip_rcp45_2040_2069_sd),precip_rcp45_2070_2099_sd=np.asarray(precip_rcp45_2070_2099_sd),
	swe_rcp85_2010_2039_rd=np.asarray(swe_rcp85_2010_2039_rd),swe_rcp85_2040_2069_rd=np.asarray(swe_rcp85_2040_2069_rd),swe_rcp85_2070_2099_rd=np.asarray(swe_rcp85_2070_2099_rd),
        swe_rcp85_2010_2039_tr=np.asarray(swe_rcp85_2010_2039_tr),swe_rcp85_2040_2069_tr=np.asarray(swe_rcp85_2040_2069_tr),swe_rcp85_2070_2099_tr=np.asarray(swe_rcp85_2070_2099_tr),
        swe_rcp85_2010_2039_sd=np.asarray(swe_rcp85_2010_2039_sd),swe_rcp85_2040_2069_sd=np.asarray(swe_rcp85_2040_2069_sd),swe_rcp85_2070_2099_sd=np.asarray(swe_rcp85_2070_2099_sd),
        precip_rcp85_2010_2039_rd=np.asarray(precip_rcp85_2010_2039_rd),precip_rcp85_2040_2069_rd=np.asarray(precip_rcp85_2040_2069_rd),precip_rcp85_2070_2099_rd=np.asarray(precip_rcp85_2070_2099_rd),
        precip_rcp85_2010_2039_tr=np.asarray(precip_rcp85_2010_2039_tr),precip_rcp85_2040_2069_tr=np.asarray(precip_rcp85_2040_2069_tr),precip_rcp85_2070_2099_tr=np.asarray(precip_rcp85_2070_2099_tr),
        precip_rcp85_2010_2039_sd=np.asarray(precip_rcp85_2010_2039_sd),precip_rcp85_2040_2069_sd=np.asarray(precip_rcp85_2040_2069_sd),precip_rcp85_2070_2099_sd=np.asarray(precip_rcp85_2070_2099_sd))
