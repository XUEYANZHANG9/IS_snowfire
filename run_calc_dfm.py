#!/bin/python 

import numpy as np
import pandas as pd 
import os
import subprocess
from subprocess import call  

#regions = ["cascades","california","northernrockies","southernrockies","whites","missouri","nwinterior","coastalnorth","coastalsouth","greatbasin","lowercolorado"]
scenarios = ["historical","rcp45","rcp85"] 
#models = ["NorESM1-M", "CNRM-CM5", "CSIRO-Mk3-6-0", "CanESM2", "MIROC5", "bcc-csm1-1-m", "HadGEM2-CC365", "HadGEM2-ES365", "CCSM4", "IPSL-CM5A-MR"]

models = ["CanESM2"]
#scenarios = ["historical"]
regions = ["whites"]

direc = '/raid9/gergel/agg_snowpack/gridcells_is_paper'

#data = pd.read_csv(os.path.join(direc,filename))
#lats = data['lat_whites']
#lons = data['lon_whites']

qsub_script = "qsub_calc_dfm.sh"

for model in models: 
	for scenario in scenarios:
		for region in regions:  
			filename = '%s.csv' % region
			data = pd.read_csv(os.path.join(direc,filename))  
			lat_name = 'lat_%s' % region 
			lon_name = 'lon_%s' % region 
			lats = data[lat_name]
			lons = data[lon_name] 
			for gridcell in np.arange(len(lats)):
				qsub_call = "qsub -v model=%s,scenario=%s,lat=%s,lon=%s %s" % (model,scenario,str(lats[gridcell]),str(lons[gridcell]),qsub_script)
				call(qsub_call, shell=True)	
	
