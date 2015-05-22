#!/bin/python 

import numpy as np
import os
import sys
from snowpack_functions import lat_lon_adjust,mask_latlon,historical_sum_swe
import glob
from scipy import stats
import datetime 
import pandas as pd
from vic_functions import get_snow_band,find_gridcell
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

## function to get elevation for snotel site 
def get_snotel_elevation(site_id):
	snotel_file = '/raid9/gergel/vic_sim_obs/snotel_data/station.info'
	snotel = np.loadtxt(snotel_file,dtype='str',delimiter = '\t') ## data is [ latitude longitude elevation snotel_id name_of_site] 
	for site in np.arange(len(snotel)): 
		line = snotel[site].split()
		if line[3] == site_id:
			elev = line[2]
			lat = line[0]
			lon = line[1]
	return(elev,lat,lon) 

## step 1: get basin from input arguments 
args = sys.argv[1:]
basin = args[0]

## step 2: for each snotel site, extract elevation band from vic simulations closest to snotel elevation

## further mask out latlons that aren't part of the masks defined by lat_lon_adjust and mask_latlon 
direc = '/raid9/gergel/agg_snowpack/snotel_vic/vic_output/%s' %basin 
site_ids = list()
for filename in os.listdir(direc): ## get list of snotel site ids 
	site_ids.append(filename)
if "11H59S" in site_ids: ## this is a missing snotel station in the Southern Rockies (i.e. it exists but isn't in Mu's drought monitoring dataset) 
	site_ids.remove("11H59S")
arr_site_ids = np.asarray(site_ids) ## make list of site ids into array 
vic_swe_elevs = list()
vic_swe = list() ## array for holding full time series of simulated swe for each snotel (average over 4 surrounding grid cells) 
for site in arr_site_ids: ## loop through snotel sites for mountain range 
	vic_site_swe = list() 
        direcsite = '/raid9/gergel/agg_snowpack/snotel_vic/vic_output/%s/%s/fluxes__*' %(basin,site)
        for pathfile in glob.glob(direcsite): ## loop through 4 simulated grid cells around each vic snotel site 
                path,fname = os.path.split(pathfile)
                elev,lat,lon = get_snotel_elevation(site) ## get elevation, latitude and longitude of snotel site
                snow_band,lat,lon = get_snow_band(fname,elev) ## get which snowband to use for snotel elevation
                mask1 = lat_lon_adjust(float(lat),float(lon),basin) ## apply first lat/lon mask
                mask2 = mask_latlon(float(lat),float(lon),basin) ## apply second lat/lon mask
                # mask3 = historical_sum_swe(j,k) ## apply historical mean swe mask (using Livneh)
                if mask1 and mask2: ## apply further masking: include grid cell IF within mask
                        if snow_band == 0:
                                data = np.loadtxt(pathfile,dtype='float',usecols=(3,),delimiter='\t')
                        elif snow_band == 1:
                                data = np.loadtxt(pathfile,dtype='float',usecols=(4,),delimiter='\t')
                        elif snow_band == 2:
                                data = np.loadtxt(pathfile,dtype='float',usecols=(5,),delimiter='\t')
                        elif snow_band == 3:
                                data = np.loadtxt(pathfile,dtype='float',usecols=(6,),delimiter='\t')
                        else:
                                data = np.loadtxt(pathfile,dtype='float',usecols=(7,),delimiter='\t')
			vic_site_swe.append(data[:]) 
	vic_swe.append(np.mean(np.asarray(vic_site_swe),axis=0)) ## append the average simulated swe for snotel site 
	vic_swe_elevs.append(elev)  ## append elevation of snotel site 

## convert to array 
vic_swe = np.asarray(vic_swe) ##[number of snotel stations,daily swe] 

## step 4: load snotel data, deal with missing values, average over all snotel data for the basin
## full array
################ create full datetime array for indexing into vic and snotel swe arrays later on 
base = datetime.datetime(1987, 1, 1)
## end date + 1 (will only produce specified end date - 1)
end_date = datetime.datetime(2006, 1, 1)
arr_dates = [base + datetime.timedelta(days=i) for i in range(0, (end_date-base).days)]
direc_snotel = '/raid9/gergel/vic_sim_obs/snotel_data/US_swe'
snotel_swe = list()
#snotel_swe = np.ndarray(shape=(len(arr_site_ids),len(arr_dates)),dtype=float) 
rowcount = 0
for site in arr_site_ids: 
	snotel_site_swe = list()
	snotel_dates = list()
	print(site) 
	filename = 'swe.%s.dat' %site
	elev,lat,lon = get_snotel_elevation(site) ## get elevation of snotel site 
	lat_sno,lon_sno = find_gridcell(float(lat),float(lon)) ## figure out which gridcell the snotel site is in 
	mask3 = lat_lon_adjust(float(lat_sno),float(lon_sno),basin) ## apply first lat/lon mask
	mask4 = mask_latlon(float(lat_sno),float(lon_sno),basin) ## apply second lat/lon mask 
	if mask3 and mask4: 
		snotel_data = np.loadtxt(os.path.join(direc_snotel,filename),dtype='str',delimiter='\t')
		for day in np.arange(len(snotel_data)):
			eachday = snotel_data[day].split()
			if np.float(eachday[0][:4]) >= 1987 and np.float(eachday[0][:4]) <= 2005: 
				snotel_dates.append(datetime.datetime.strptime(eachday[0],'%Y%m%d'))
				snotel_site_swe.append(np.float(eachday[1]))
		arr_snotel_site_swe = np.asarray(snotel_site_swe)
		print(len(arr_snotel_site_swe)) 
		arr_snotel_site_swe[arr_snotel_site_swe < 0]=np.nan ## change -99 values in swe to nan
		# snotel_swe.append(arr_snotel_site_swe) 
		## deal with missing values using pandas merge
		df_full = pd.DataFrame({'cola':arr_dates})
		df_part = pd.DataFrame({'cola':snotel_dates,'swe':arr_snotel_site_swe.tolist()}) 
		## now join dataframes so that missing values are populated with nans
	 	new_df = df_full.merge(df_part,on=['cola'],how='left')
		a = new_df['swe'].values
		if len(a) == len(arr_dates):	
			snotel_swe.append(a) 
		#snotel_swe[rowcount,:] = a 
		print(len(new_df['swe'].values))
		rowcount += 1

## convert snotel list into array 
arr_snotel_swe = np.asarray(snotel_swe) ## [number of snotel stations,daily swe] 
arr_snotel_swe[arr_snotel_swe < 0] = np.nan ## if swe values are below zero, convert to nans 
print(arr_snotel_swe.shape) 

## step 5: extract April 1 swe from vic and obs time series and average over the time period 
april_dates = list()
april_index = list() 
for dayy in np.arange(len(arr_dates)):
	if arr_dates[dayy].month == 4 and arr_dates[dayy].day == 1:
		april_index.append(dayy) 
		april_dates.append(arr_dates[dayy])
april_index = np.asarray(april_index) ## this is an index array
april_index_array = np.repeat(april_index.reshape(1,len(april_index)),len(vic_swe),axis=0) ## create index array for getting april values from vic and snotel swe 
vicswe_april = np.take(vic_swe,april_index_array)
snotelswe_april = np.take(arr_snotel_swe,april_index_array)
## average over time period 
vicswe_april_avg = np.mean(vicswe_april,axis=1)
snotelswe_april_avg = np.mean(snotelswe_april,axis=1)  
######################################################## step 6: plot snotel data and vic simulations ############################################################

## plot April 1 SWE 
plt.figure(figsize=(16,4))
## get April 1 SWE from above vic and snotel arrays
april_vic = list()
april_snotel = list()
for dayy in np.arange(len(arr_dates)): 
	if arr_dates[dayy].month == 4 and arr_dates[dayy].day == 1: 
		april_dates.append(arr_dates[dayy])
		april_vic.append(avg_vic[dayy])
		april_snotel.append(avg_snotel[dayy])
plt.plot(april_dates,april_vic,'b-',label='vic')
plt.plot(april_dates,april_snotel,'r-',label='snotel')
plt.ylabel('SWE [mm]') 
plt.title('April 1 SWE in %s' %basin) 
plt.legend()
plotname = '%s_april1swe' %basin
savepath = os.path.join(plot_direc,plotname)
print("saving figure to '%s'" %savepath)
plt.savefig(savepath) 

