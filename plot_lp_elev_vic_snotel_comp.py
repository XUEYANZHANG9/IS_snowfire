#!/bin/python 

import numpy as np
import os
import sys
from snowpack_functions import lat_lon_adjust,mask_latlon,historical_sum_swe,mask_out_other_mtns
import glob
from scipy import stats
import datetime 
import pandas as pd
from vic_functions import get_snow_band,find_gridcell
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from scipy.stats import nanmean 

################### set fontsize ###############
fs = 20 ## font size
ls = 15 ## legend size
################################################

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

## create figure
fig = plt.figure(figsize=(18,10))
## loop over basins 
basins = ['cascades','california','northernrockies','southernrockies','whites']
num = 1
for basin in basins: 

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
			#mask1 = lat_lon_adjust(float(lat),float(lon),basin) ## apply first lat/lon mask
			mask1 = mask_out_other_mtns(float(lat),float(lon)) ## apply lat/lon mask
			#mask2 = mask_latlon(float(lat),float(lon),basin) ## apply second lat/lon mask
			# mask3 = historical_sum_swe(j,k) ## apply historical mean swe mask (using Livneh)
			if mask1: ## apply further masking: include grid cell IF within mask
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
				if len(data[:]) > 0:
					vic_site_swe.append(data[:]) 
		swe_toappend = nanmean(np.asarray(vic_site_swe),axis=0)
		if type(swe_toappend) != np.float64: 
			vic_swe.append(nanmean(np.asarray(vic_site_swe),axis=0)) ## append the average simulated swe for snotel site 
			vic_swe_elevs.append(elev)  ## append elevation of snotel site
		else:  
			site_ids.remove(site) ## if that site is producing nans, eliminate it from the snotel site list 
	## eliminate any sites that had nans
	arr_site_ids = np.asarray(site_ids) ## make list of site ids into array

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
		if (basin == "whites"):
			if arr_dates[dayy].month == 2 and arr_dates[dayy].day == 1:
				april_index.append(dayy)
				april_dates.append(arr_dates[dayy])
		else: 
			if arr_dates[dayy].month == 4 and arr_dates[dayy].day == 1:
				april_index.append(dayy) 
				april_dates.append(arr_dates[dayy])
	april_index = np.asarray(april_index) ## this is an index array
	april_index_array = np.repeat(april_index.reshape(1,len(april_index)),len(vic_swe),axis=0) ## create index array for getting april values from vic and snotel swe 
	vicswe_april = np.take(vic_swe,april_index,axis=1)
	snotelswe_april = np.take(arr_snotel_swe,april_index,axis=1)
	## average over time period 
	vicswe_april_avg = np.mean(vicswe_april,axis=1)
	snotelswe_april_avg = nanmean(snotelswe_april,axis=1)  

	################################################ do elevation binning #########################################################################
	swe_500 = list()
	swe_800 = list()
	swe_1100 = list()
	swe_1400 = list()
	swe_1700 = list()
	swe_2000 = list()
	swe_2300 = list()
	swe_2600 = list()
	swe_2900 = list()
	swe_3200 = list()
	swe_3500 = list()
	swe_3800 = list()

	elvs = [500,800,1100,1400,1700,2000,2300,2600,2900,3200,3500,3800]
	swees = [swe_500,swe_800,swe_1100,swe_1400,swe_1700,swe_2000,swe_2300, swe_2600, swe_2900, swe_3200, swe_3500, swe_3800] 
	for elv,vicswe,snotelswe in zip(vic_swe_elevs,vicswe_april_avg,snotelswe_april_avg):
		ind = np.argmin(np.abs((np.asarray(elvs) - np.float(elv))))
		swees[ind].append([vicswe,snotelswe]) 
	######################################################## step 6: plot snotel data and vic simulations ############################################################
	ax = fig.add_subplot(1,5,num) ## need to deal with this plotting number later
	## swe on x axis, elevation on y axis with 40 m offset for snotel and vic 
	lw = 2.0
	count1 = 0
	for swe in swees: 
		if len(swe) > 0:  
			swearr = np.asarray(swe) 
			sim = swearr[:,0]
			obs = swearr[:,1] 
			simobs = [sim,obs] 
			colours = ['b','k'] 
			count = 0
			for so in simobs: 
				meanswe = np.mean(so)
				# print(so) 
				minswe = np.min(so)
				maxswe = np.max(so)
				swe10 = np.percentile(so,10)
				swe90 = np.percentile(so,90) 
				## plot
				if (count == 0): ## for vic, plot actual elevation 
					elevmet = elvs[count1]
				else: ## for snotel, plot actual elevation with 40 m offset
					elevmet = elvs[count1] - 40
				xmin = np.arange(minswe,swe10,1)
				ax.plot(xmin,np.ones(len(xmin))*elevmet,color=colours[count],linestyle='--',linewidth=lw)
				xmax = np.arange(swe90,maxswe,1)
				ax.plot(xmax,np.ones(len(xmax))*elevmet,color=colours[count],linestyle='--',linewidth=lw)
				## 10-90 range
				xmid = np.arange(swe10,swe90,1)
				if (count == 0) and (count1 == 7):
					ax.plot(xmid,np.ones(len(xmid))*elevmet,label='Simulated',color=colours[count],linestyle='-',linewidth=lw)
					ax.plot(meanswe,elevmet,'o',label='Mean Simulated',color=colours[count])
					ax.plot(swe10,elevmet,'s',label='Simulated 10th Percentile',color=colours[count])
					ax.plot(swe90,elevmet,'s',label='Simulated 90th Percentile',color=colours[count])
				elif (count == 1) and (count1 == 7):
					ax.plot(xmid,np.ones(len(xmid))*elevmet,label='Observed',color=colours[count],linestyle='-',linewidth=lw)
					ax.plot(meanswe,elevmet,'o',label='Mean Observed',color=colours[count])
					ax.plot(swe10,elevmet,'s',label='Observed 10th Percentile',color=colours[count])
					ax.plot(swe90,elevmet,'s',label='Observed 90th Percentile',color=colours[count])
				else:
					ax.plot(xmid,np.ones(len(xmid))*elevmet,color=colours[count],linestyle='-',linewidth=lw)
                                        ax.plot(meanswe,elevmet,'o',color=colours[count])
                                        ax.plot(swe10,elevmet,'s',color=colours[count])
                                        ax.plot(swe90,elevmet,'s',color=colours[count])
				if (basin == "whites") and (count1 == 7):
					ax.legend(loc='lower right',prop={'size':ls}) 
				
				count += 1
		count1 += 1
	#if (basin == "whites"):
	import matplotlib.patches as mpatches

	red_patch = mpatches.Patch(color='red', label='Simulated')
	green_patch = mpatches.Patch(color='green', label='Observed')

	#ax.legend(handles=[red_patch,green_patch],bbox_to_anchor=(1.1, 1.05), loc=2)
	#ax.legend(loc='upper right',handles=[red_patch,green_patch],shadow=True)
	if (num == 1):
		ax.set_ylabel('Elevation [m]',size=fs) 
	if (num == 3):
		ax.set_xlabel('SWE [mm]',size=fs) 
	ax.set_ylim([0,3500]) 

	## set x ticks #######
	if (basin == "northernrockies") or (basin == "california") or (basin == "southernrockies"):
		ax.set_xticks([0,400,800,1200]) 
	elif (basin == "whites"):
		ax.set_xticks([0,75,150,225])
	else:
		ax.set_xticks([0,2000,4000])  
	ax.xaxis.set_tick_params(labelsize=fs)	

	## set y ticks #######
	if (basin != "cascades"): 
		plt.setp(ax.get_yticklabels(), visible=False)
		ax.yaxis.set_tick_params(labelsize=fs)		

	if (basin == "california"):
		ax.set_title('Sierra Nevada')
	elif (basin == "cascades"):
		ax.set_title('Cascades')
	elif (basin == "northernrockies"):
		ax.set_title('Northern Rockies')
	elif (basin == "southernrockies"):
		ax.set_title('Southern Rockies')
	else:
		ax.set_title('White Mountains') 
	#plt.legend()
	num += 1 
# fig.legend(handles=[red_patch,green_patch],loc=2) 
plot_direc = '/raid9/gergel/agg_snowpack/snotel_vic/plots'
plotname = 'binned_allbasins_april1swe' 
savepath = os.path.join(plot_direc,plotname)
print("saving figure to '%s'" %savepath)
plt.savefig(savepath,dpi=300) 

