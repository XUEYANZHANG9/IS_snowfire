#!/bin/python 

import numpy as np
import sys
import os
import math
from snowpack_functions import lat_lon_adjust,unpack_netcdf_swe_month,mask_latlon,unpack_netcdf_file_var,historical_sum_swe
from scipy import ndimage 
## get command line arguments 
args = sys.argv[1:]
basin = args[0]
scenario = args[1]
direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin
file_swe = 'SWE_ensavg_%s_%s.nc' %(scenario,basin)
lats,lons,swe,datess = unpack_netcdf_file_var(direc,file_swe,"swe")

## step 1: load data sources 
## PET: all three: NatVeg, Short, Tall
## AET: evaporation plus transpiration 

## compare pet and aet from VIC (then see about computing aet using pm reference et) 
pet_agg = list()
aet_agg = list()
lats_inc = list()
lons_inc = list()

direc = '/raid9/gergel/agg_snowpack/goodleap/%s' %basin
## filename
file_petnat = '%s_ensavg_%s_%s.nc' %("PET_NatVeg",scenario,basin)
file_petshort = '%s_ensavg_%s_%s.nc' %("PET_Short",scenario,basin)
file_pettall = '%s_ensavg_%s_%s.nc' %("PET_Tall",scenario,basin)
file_evap = '%s_ensavg_%s_%s.nc' %("Evaporation",scenario,basin)
file_transp = '%s_ensavg_%s_%s.nc' %("Transp",scenario,basin)
### select daily swe data based on time chunk
if (chunk == "1970-1999"):
	years1 = "1970_1979"
	years2 = "1980_1989"
	years3 = "1990_1999"
elif (chunk == "2010-2039"):
	years1 = "2010_2019"
        years2 = "2020_2029"
        years3 = "2030_2039"
elif (chunk == "2040-2069"):
	years1 = "2040_2049"
        years2 = "2050_2059"
        years3 = "2060_2069"
else: 
	years1 = "2070_2079"
        years2 = "2080_2089"
        years3 = "2090_2099"
file_dailyswe1 = 'dailyswe_%s_%s.nc' %(scenario,years1)
file_dailyswe2 = 'dailyswe_%s_%s.nc' %(scenario,years2)
file_dailyswe3 = 'dailyswe_%s_%s.nc' %(scenario,years3) 

## load data for pet/aet analysis
lats,lons,petnat,datess_petnat = unpack_netcdf_file_var(direc,file_petnat,"PET_NatVeg")
lats,lons,petshort,datess_petshort = unpack_netcdf_file_var(direc,file_petshort,"PET_Short")
lats,lons,pettall,datess_pettall = unpack_netcdf_file_var(direc,file_pettall,"PET_Tall")
lats,lons,evap,datess_evap = unpack_netcdf_file_var(direc,file_evap,"Evaporation")
lats,lons,transp,datess_transp = unpack_netcdf_file_var(direc,file_transp,"Transp")

## load daily SWE data
direc_dailyswe = '/raid9/gergel/agg_snowpack/goodleap/dailySWE' 
lats,lons,swe1,datess_swe1 = unpack_netcdf_file_var(direc_dailyswe,file_dailyswe1,"swe")
lats,lons,swe2,datess_swe2 = unpack_netcdf_file_var(direc_dailyswe,file_dailyswe2,"swe")
lats,lons,swe3,datess_swe3 = unpack_netcdf_file_var(direc_dailyswe,file_dailyswe3,"swe")

## adjust data for hydro years 
petnat = petnat[9:-2,:,:]
petshort = petshort[9:-2,:,:]
pettall = pettall[9:-2,:,:]
evap = evap[9:-2,:,:]
transp = transp[9:-2,:,:]
for j in np.arange(len(lats)): ## loop over latitude
	for k in np.arange(len(lons)): ## loop over longitude
		### don't calculate area for missing value elements
                if (math.isnan(swe[0,j,k])) == False:
			if_in_box = mask_latlon(lats[j],lons[k],basin)
			adjust_mask = lat_lon_adjust(lats[j],lons[k],basin)
			mean_swe = historical_sum_swe(lats[j],lons[k]) 
			## new historical swe function based on livneh instead of vic simulations 
			if if_in_box and adjust_mask and mean_swe:
				petsum = 0
				aetsum = 0
				for i in np.arange(len(swe)): ## now loop over year 
					ind = i*12
					petsum += np.sum(np.asarray(petnat[ind:ind+12,j,k])) + np.sum(np.asarray(petshort[ind:ind+12,j,k])) + np.sum(np.asarray(pettall[ind:ind+12,j,k]))
					aetsum += np.sum(np.asarray(evap[ind:ind+12,j,k])) + np.sum(np.asarray(transp[ind:ind+12,j,k]))
				pet_agg.append(petsum/len(swe))
				aet_agg.append(aetsum/len(swe)) 
				lats_inc.append(lats[j])
				lons_inc.append(lons[k])

				###################### NOW FIGURE OUT SNOWMELT DATE AND STATISTICS ####################################
				## concatenate daily swe and dates values, take diff of swe values 
				dayswe = np.concatenate((np.asarray(swe1[:,j,k]),np.asarray(swe2[:,j,k]),np.asarray(swe3[:,j,k])),axis=0)  
				datesswe = np.concatenate((datess_swe1,datess_swe2,datess_swe3),axis=0)
				## make index of dataframe be dates
				df = pd.DataFrame(index=datesswe) 
				df['colb'] = dayswe 
				## eliminate months earlier than July 
				df_half = df[df.index.month < 7] 
				## group data by year 
				s = df_half.groupby(lambda x: x.year)
				## calculate center of mass of the diff of each year (snowmelt) and round its_centers = s['colb'].apply(lambda x: np.round(ndimage.measurements.center_of_mass(np.diff(x))))
				s_centers = s['colb'].apply(lambda x: np.round(ndimage.measurements.center_of_mass(np.diff(x))))
				

### save arrays to files 
filearrayname = '/raid9/gergel/agg_snowpack/%s/moistdef_%s.npz' %(scenario,basin) 
np.savez(filearrayname,lats=np.asarray(lats_inc),lons=np.asarray(lons_inc),pet=np.asarray(pet_agg),aet=np.asarray(aet_agg))
print("finished analysis for %s %s" %(scenario,basin)) 			 

