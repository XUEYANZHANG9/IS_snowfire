#!/bin/python 

import sys
import os
import numpy as np
import shutil
import subprocess
from vic_functions import find_gridcell, four_nearest_neighbors,set_norun_gridcells,all_nearest_neighbors 
basin,upper_lat,lower_lat,left_lon,right_lon = sys.argv[1:] ## boundaries of basin 

## step two: find all snotel sites that are inside these boundaries (for Western US, so no Canada ones) and add to dictionary, with elevation as value (snotel id as key), add lats and lons to lists too
snotel_file = '/raid9/gergel/vic_sim_obs/snotel_data/station.info' 
snotel = np.loadtxt(snotel_file,dtype='str',delimiter = '\t') ## data is [ latitude longitude elevation snotel_id name_of_site] 
site_elev = {} ## initialize dict for site_id (key) elevation (value) info
snotel_lats = list()
snotel_lons = list()
snotel_ids = list()
for eachline in np.arange(len(snotel)):
	site = snotel[eachline].split()
	if float(site[0]) > float(lower_lat) and float(site[0]) < float(upper_lat) and float(site[1]) > float(left_lon) and float(site[1]) < float(right_lon):
		site_elev[site[3]] = float(site[2]) ## add site id and elev to dict 
		snotel_lats.append(site[0])
		snotel_lons.append(site[1])
		snotel_ids.append(site[3])

## step three: find grid cell that each snotel site is in, and then generate all neighboring grid cells for each snotel site. 
arr_snotel_lats = np.asarray(snotel_lats)
arr_snotel_lons = np.asarray(snotel_lons)
arr_snotel_ids = np.asarray(snotel_ids)
for latlon in np.arange(len(arr_snotel_lats)):
	lat_gridcell,lon_gridcell = find_gridcell(float(arr_snotel_lats[latlon]),float(arr_snotel_lons[latlon]))
	# u_r,l_r,u_l,l_l = four_nearest_neighbors(lat_gridcell,lon_gridcell)
	###
	lats_array,lons_array = all_nearest_neighbors(lat_gridcell,lon_gridcell) 
	###
	print("now analyzing the snotel site at %s %s" %(lat_gridcell,lon_gridcell))
	'''
	lats_array = np.ndarray(shape=(4,1), dtype=float)
	lons_array = np.ndarray(shape=(4,1), dtype=float)
	lats_array[0,0] = u_r[0]
	lats_array[1,0] = l_r[0]
	lats_array[2,0] = u_l[0]
	lats_array[3,0] = l_l[0]
	lons_array[0,0] = u_r[1]
	lons_array[1,0] = l_r[1]
	lons_array[2,0] = u_l[1]
	lons_array[3,0] = l_l[1]
	'''
	new_soil_suffix = arr_snotel_ids[latlon]
	soil_name = "soil" + new_soil_suffix 
	direc = '/raid9/gergel/agg_snowpack/snotel_vic/soil_files'
	new_soil_file = os.path.join(direc,soil_name)
	soil_params = '/raid9/gergel/vic_sim_obs/data_from_Matt/soil_file'
	set_norun_gridcells(soil_params,lats_array,lons_array,new_soil_suffix) #### step four: prepare soil file to run over only those  grid cells
	## step five: change global parameter file with a) proper soil parameter file and b) proper results directory using snotel id 
	old_global_param_file = "/raid9/gergel/agg_snowpack/snotel_vic/global_files/4.1.2.k"
	new_global_param_file = "/raid9/gergel/agg_snowpack/snotel_vic/global_files/%s" %("global_file" + arr_snotel_ids[latlon]) 
	shutil.copyfile(old_global_param_file, new_global_param_file) ## copy global parameter file to new global parameter file path for editing 
	result_dir = '/raid9/gergel/agg_snowpack/snotel_vic/vic_output/%s/%s' %(basin,arr_snotel_ids[latlon]) 
	if not os.path.exists(result_dir): ## if results directory doesn't exist, create it
		os.makedirs(result_dir)
	result_str = '<RESULT_DIR>'
	soil_str = '<SOIL_DIR>'
	with open(new_global_param_file,"wt") as fout: ## change global parameter file to include the correct paths 
		with open(old_global_param_file,"rt") as fin:
			for line in fin: 
				if result_str in line:
					fout.write(line.replace(result_str,result_dir,1))
				elif soil_str in line: 
					fout.write(line.replace(soil_str,new_soil_file,1))
				else: 
					fout.write(line) 			
	## step six: run vic 
	print("now running VIC 4.1.2m for 4 grid cells surrounding Snotel site %s" %arr_snotel_ids[latlon])
	#subprocess.call(["/raid9/gergel/vic_sim_obs/source_code/VIC-VIC.4.1.2.m/src/vicNl -g", new_global_param_file],shell=True) 
	subprocess.call("/raid9/gergel/vic_sim_obs/source_code/VIC-VIC.4.1.2.m/src/vicNl -g"+new_global_param_file,shell=True)
## step seven: average over all snotel sites, average over all vic runs (using elevation bands) 
###### do this in separate script #########
## step eight: plot the two time series 




