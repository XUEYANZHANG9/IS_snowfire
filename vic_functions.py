#!/bin/python 

import sys
args = sys.argv[0]
arg1 = args[0]
arg2 = args[1]
arg3 = args[2]
def set_norun_gridcells(soil_file,lats,lons,new_soil_file_name):
	### input: numpy array of lats, numpy array of lons (both as floats)
	import numpy as np
	import os
	## load VIC soil parameters text file
	soil_params = np.loadtxt(soil_file, dtype = 'str', delimiter = ',')
	## create output file
	fname = "soil" + new_soil_file_name
	direc = '/raid9/gergel/agg_snowpack/snotel_vic/soil_files'
	new_soil_file = os.path.join(direc,fname)
	### .split() splits the line up by whitespace!! to convert to float: float(string value)
    	######################### 2nd column: latitude; 3rd column: longitude; 21st column: average elevation of grid cell
	## set 1s to 0s so that grid cells that aren't in the input array aren't run 
	count = 0
	with open(new_soil_file,"wt") as fout:
		with open(soil_file,"rt") as fin: 
			for line in fin: 
				gridcell_entry = soil_params[count].split()
				## get indices of grid cells in lats/lons
				ind_lat = [i for (i, val) in enumerate(lats) if val == float(gridcell_entry[2])]
				ind_lon = [i for (i, val) in enumerate(lons) if val == float(gridcell_entry[3])]
				intersec = set(np.asarray(ind_lat)).intersection(np.asarray(ind_lon))
				if float(gridcell_entry[2]) not in lats and float(gridcell_entry[3]) not in lons:
					fout.write(line.replace('1', '0', 1))
				elif float(gridcell_entry[2]) in lats and float(gridcell_entry[3]) not in lons: 
					fout.write(line.replace('1', '0', 1))
				elif float(gridcell_entry[2]) not in lats and float(gridcell_entry[3]) in lons:
					fout.write(line.replace('1', '0', 1))
				elif float(gridcell_entry[2]) in lats and float(gridcell_entry[3]) in lons and len(intersec) == 0:
					fout.write(line.replace('1', '0', 1))
				elif float(gridcell_entry[2]) in lats and float(gridcell_entry[3]) in lons and len(intersec) > 0:
					fout.write(line)
					print('this grid cell %s, %s is included in the input array' %(gridcell_entry[2],gridcell_entry[3]))
				count += 1

## test function to see if I can call a python function directly in a shell script and give it input arguments 
def test_function(num1=arg1,num2=arg2,num3=arg3):
	print(num1)
	print(num2)
	print(num3)

if __name__ == "__main__":
	test_function()

def four_nearest_neighbors(lat,lon):
	import numpy as np
	dg = 0.0625
	upper_right = np.asarray([lat + dg, lon + dg])
	upper_left = np.asarray([lat + dg, lon - dg])
	lower_right = np.asarray([lat - dg, lon + dg])
	lower_left = np.asarray([lat - dg, lon - dg])
	return(upper_right,lower_right,upper_left,lower_left) # first number in array is lat, second is lon

def all_nearest_neighbors(lat,lon): 
	## function produces arrays of lats and lons for nine grid cells surrounding snotel site: the grid cell it's located in plus all adjacent ones 
	import numpy as np
	dg = 0.0625
	lats_array = np.asarray([ lat + dg, lat + dg, lat - dg, lat - dg, lat + dg, lat, lat - dg, lat, lat ]).reshape(9,1) 
	lons_array = np.asarray([ lon + dg, lon - dg, lon + dg, lon - dg, lon, lon - dg, lon, lon + dg, lon ]).reshape(9,1)  
	## upper right, upper left, lower right, lower left, top, left, bottom, right, gridcell 
	return(lats_array,lons_array) 

def find_gridcell(lat_snotel,lon_snotel):
	import numpy as np
	import math
	gridlats = list()
	gridlons = list()
	## lat
	x = np.arange(round(lat_snotel)-1, round(lat_snotel) + 1, 0.03125)
	for i in x: 
		if round(math.modf(round((i/0.0625),5))[0],2) == 0.5: 
			gridlats.append(round(i,5))  
	grid_diff = np.asarray(gridlats) - lat_snotel
	gridmin = np.argmin(np.abs(grid_diff))
	lat_gridcell = gridlats[gridmin]
	## lon
	x = np.arange(round(lon_snotel)-1, round(lon_snotel) + 1, 0.03125)
        for i in x:
                if round(math.modf(round((i/0.0625),5))[0],2) == -0.5:
                        gridlons.append(round(i,5))
        grid_diff = np.asarray(gridlons) - lon_snotel
        gridmin = np.argmin(np.abs(grid_diff))
        lon_gridcell = gridlons[gridmin]
	return(lat_gridcell,lon_gridcell)

def get_gridcell_id(lat,lon):
        #### function gets unique gridcell number in soil file so that it can be used as index in snow band file
        import numpy as np
        soil_file = '/raid9/gergel/vic_sim_obs/data_from_Matt/soil_file'
        soil_params = np.loadtxt(soil_file,dtype='str',delimiter = ',')
        count = 0
        with open(soil_file,"rt") as fin:
                for line in fin:
                        gridcell_entry = soil_params[count].split()
                        if float(lat) == float(gridcell_entry[2]) and float(lon) == float(gridcell_entry[3]):
                                gridcell_id = gridcell_entry[1]
                        count += 1
        return(gridcell_id)

def get_snow_band(fluxfilename,snotel_elev):
        import numpy as np
        ### using the lat,lon of gridcell and the elevation of the snotel site, fctn gets the snow band that it is closest to (i.e. snow band 1, snow band 2, etc)
        text,exspace,lat,lon = fluxfilename.split('_')
        ## need gridcell number, get from above function: get_gridcell_id(lat,lon), returns gridcell id number
        gridcell_num = get_gridcell_id(lat,lon)
        snow_file = '/raid9/gergel/vic_sim_obs/data_from_Matt/newsnow.txt2'
        snow = np.loadtxt(snow_file,dtype='str',delimiter = '\t')
        for eachline in np.arange(len(snow)):
                if snow[eachline,0].strip() == gridcell_num.strip():
                        elevs = snow[eachline,2].split()
                        elevs_floats = np.array(elevs).astype(np.float)
                        snowband = np.argmin(np.abs(elevs_floats - float(snotel_elev)))
        return(snowband)

def avg_4_gridcells(arr,running_code,vicversion,id,colnum,elev):
                import numpy as np
                import os
                import glob
                direc = '/raid9/gergel/vic_sim_obs/vic_output/obs_sim/%s/%s/%s/fluxes__*' %(running_code,vicversion,id)
                arr_avg = list()
                for pathfile in glob.glob(direc):
                        path,fname = os.path.split(pathfile)
                        ## load columns that correspond to input snowband
                        snow_band = get_snow_band(fname,elev)
                        if snow_band == 0:
                                data = np.loadtxt(pathfile,dtype='float',usecols =(3,8,13,18),delimiter='\t')
                        elif snow_band == 1:
                                data = np.loadtxt(pathfile,dtype='float',usecols =(4,9,14,19),delimiter='\t')
                        elif snow_band == 2:
                                data = np.loadtxt(pathfile,dtype='float',usecols =(5,10,15,20),delimiter='\t')
                        elif snow_band == 3:
                                data = np.loadtxt(pathfile,dtype='float',usecols =(6,11,16,21),delimiter='\t')
                        else:
                                data = np.loadtxt(pathfile,dtype='float',usecols =(7,12,17,22),delimiter='\t')
                        arr_avg.append(data[:,colnum])
                avg_vals = np.mean(np.asarray(arr_avg),axis=0)
                #if (vicversion == "VIC-VIC.4.1.1"):
                #print("length of arr is %f" %round(len(arr)))
                #print("length of avg_vals is %f" %len(np.asarray(avg_vals)))
                #avg_vals = np.reshape(np.asarray(avg_vals),(round(len(arr)),2))
                #avg_vals = np.mean(np.asarray(avg_vals),axis=1)
                avg_vals_res = np.reshape(avg_vals,(len(avg_vals),1))
                #print(len(avg_vals_res))
                return(avg_vals_res)

def get_snow_band(fluxfilename,snotel_elev):
        import numpy as np
        ### using the lat,lon of gridcell and the elevation of the snotel site, fctn gets the snow band that it is closest to (i.e. snow band 1, snow band 2, etc)
        text,exspace,lat,lon = fluxfilename.split('_')
        ## need gridcell number, get from above function: get_gridcell_id(lat,lon), returns gridcell id number 
        gridcell_num = get_gridcell_id(lat,lon)
        snow_file = '/raid9/gergel/vic_sim_obs/data_from_Matt/newsnow.txt2'
        snow = np.loadtxt(snow_file,dtype='str',delimiter = '\t')
        for eachline in np.arange(len(snow)):
                if snow[eachline,0].strip() == gridcell_num.strip():
                        elevs = snow[eachline,2].split()
                        elevs_floats = np.array(elevs).astype(np.float)
                        snowband = np.argmin(np.abs(elevs_floats - float(snotel_elev)))
        return(snowband,lat,lon)

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
