#!/bin/python 

import numpy as np
import os
import sys
from snowpack_functions import lat_lon_adjust,mask_latlon 
import glob
from scipy import stats
import datetime 
import pandas as pd
from vic_functions import get_snow_band,find_gridcell
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
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

## step 1: get basin
args = sys.argv[1:]
basin = args[0]

## step 2: for each snotel site, extract elevation band from vic simulations closest to snotel elevation
## further mask out latlons that aren't part of the masks defined by lat_lon_adjust and mask_latlon 
direc = '/raid9/gergel/agg_snowpack/snotel_vic/vic_output/%s' %basin 
site_ids = list()
for filename in os.listdir(direc): ## get list of snotel site ids 
	site_ids.append(filename)
if "11H59S" in site_ids: ## this is a missing snotel station in the Southern Rockies  
	site_ids.remove("11H59S")
arr_site_ids = np.asarray(site_ids)
vic_swe = list() 
for site in arr_site_ids:
	direcsite = '/raid9/gergel/agg_snowpack/snotel_vic/vic_output/%s/%s/fluxes__*' %(basin,site)
	for pathfile in glob.glob(direcsite): 
		path,fname = os.path.split(pathfile) 
		elev,lat,lon = get_snotel_elevation(site)
		snow_band,lat,lon = get_snow_band(fname,elev) ## get which snowband to use for snotel elevation
		mask1 = lat_lon_adjust(float(lat),float(lon),basin)
		mask2 = mask_latlon(float(lat),float(lon),basin)
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
			vic_swe.append(data[:]) ## add to vic swe list 

## step 3: average over all vic simulations 
avg_vic = np.mean(np.asarray(vic_swe),axis=0)
print(avg_vic.shape)
## step 4: load snotel data, deal with missing values, average over all snotel data for the basin
## full array
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
	elev,lat,lon = get_snotel_elevation(site)
	lat_sno,lon_sno = find_gridcell(float(lat),float(lon))
	mask3 = lat_lon_adjust(float(lat_sno),float(lon_sno),basin)
	mask4 = mask_latlon(float(lat_sno),float(lon_sno),basin)
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
## calculate average of snotel swe 
arr_snotel_swe = np.asarray(snotel_swe)
print(arr_snotel_swe.shape) 
avg_snotel = stats.nanmean(arr_snotel_swe,axis=0)
avg_snotel[avg_snotel < -100]=np.nan
avg_snotel[avg_snotel < -5]=np.nan 
print(avg_snotel.shape) 
######################################################## step 5: plot snotel data and vic simulations ############################################################
## plot all data
plt.figure(figsize=(16,4))
plt.plot(arr_dates,avg_vic,'b-',label='vic')
plt.plot(arr_dates,avg_snotel,'r-',label='snotel')
plt.legend() 
plt.ylabel('SWE [mm]') 
plt.title('SWE in %s' %basin) 
plot_direc = '/raid9/gergel/agg_snowpack/snotel_vic/plots'
plotname = '%s_all' %basin
savepath = os.path.join(plot_direc,plotname)
print("saving figure to '%s'" % savepath)
plt.savefig(savepath) 

## plot April 1 SWE 
plt.figure(figsize=(16,4))
## get April 1 SWE from above vic and snotel arrays
april_dates = list()
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

## plot maximum SWE every year (actual SWE and julian day) 
year_range = np.arange(base.year,end_date.year,step=1)
max_vic = list()
max_snotel = list()
max_snotel_dates = list()
max_snotel_julian = list()
max_vic_dates = list()
max_vic_julian = list()
for yearr in year_range: 
	max_vic_list = list()
	max_snotel_list = list()
	max_date_list = list()
	for dayyy in np.arange(len(avg_vic)):
		if arr_dates[dayyy].year == yearr:
			max_vic_list.append(avg_vic[dayyy])
			max_snotel_list.append(avg_snotel[dayyy])
			max_date_list.append(arr_dates[dayyy]) 
	max_vic.append(np.nanmax(np.asarray(max_vic_list)))
	max_snotel.append(np.nanmax(np.asarray(max_snotel_list)))
	max_snotel_date = np.asarray(max_date_list)[np.nanargmin(np.asarray(max_vic_list))]
	max_vic_date = np.asarray(max_date_list)[np.nanargmin(np.asarray(max_snotel_list))]
	max_vic_dates.append(max_vic_date)
	max_snotel_dates.append(max_snotel_date)
	max_snotel_julian.append(max_snotel_date.timetuple().tm_yday) ## convert datetime to julian day
	max_vic_julian.append(max_vic_date.timetuple().tm_yday) ## convert datetime to julian day 

## plot
plt.figure(figsize=(16,4))
plt.plot(max_vic_dates,max_vic,'bs',markersize=7,label='vic')
plt.plot(max_snotel_dates,max_snotel,'r*',markersize=7,label='snotel')
plt.title('Maximum Yearly SWE in %s' %basin) 
plt.ylabel('SWE [mm]') 
plt.legend()
plotname = '%s_maxswe' %basin 
savepath = os.path.join(plot_direc,plotname)
print("saving figure to '%s'" %savepath) 
plt.savefig(savepath) 

## plot
plt.figure(figsize=(16,4))
plt.plot(year_range.reshape(len(year_range),),max_vic_julian,'b-',label='vic')
plt.plot(year_range.reshape(len(year_range),),max_snotel_julian,'r-',label='snotel')
plt.title('Julian day of Maximum Yearly SWE in %s' %basin)
plt.ylabel('Julian Day')
plt.legend()
plotname = '%s_julian_maxswe' %basin
savepath = os.path.join(plot_direc,plotname)
print("saving figure to '%s'" %savepath)
plt.savefig(savepath) 
