#!/bin/python 

import numpy as np
import os
import sys
from snowpack_functions import lat_lon_adjust,mask_latlon 
import glob 
from vic_functions import get_snow_band,find_gridcell

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
## step 4: load snotel data, deal with missing values, average over all snotel data for the basin
direc_snotel = '/raid9/gergel/vic_sim_obs/snotel_data/US_swe'
snotel_swe = list()
snotel_dates = list()
for site in arr_site_ids: 
	snotel_site_swe = list()
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
		arr_snotel_site_swe[arr_snotel_site_swe==-99]=np.nan ## change -99 values in swe to nan
		snotel_swe.append(arr_snotel_site_swe) 
## calculate average of snotel swe 
avg_snotel = np.mean(snotel_swe[~np.isnan(snotel_swe)],axis=0) 
## step 5: plot snotel data and vic simulations 



