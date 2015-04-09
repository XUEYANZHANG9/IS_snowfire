#!/bin/python 

import numpy as np
from snowpack_functions import lat_lon_adjust,unpack_netcdf_swe_month,mask_latlon,unpack_netcdf_file_var,historical_sum_swe
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

## load data  
lats,lons,petnat,datess_petnat = unpack_netcdf_file_var(direc,file_petnat,"petnat")
lats,lons,petshort,datess_petshort = unpack_netcdf_file_var(direc,file_petshort,"petshort")
lats,lons,pettall,datess_pettall = unpack_netcdf_file_var(direc,file_pettall,"pettall")
lats,lons,evap,datess_evap = unpack_netcdf_file_var(direc,file_evap,"evap")
lats,lons,transp,datess_transp = unpack_netcdf_file_var(direc,file_transp,"transp")

## adjust data for hydro years 
petnat = petnat[9:-2,:,:]
petshort = petshort[9:-2,:,:]
pettall = pettall[9:-2,:,:]
evap = evap[9:-2,:,:]
transp = transp[9:-2,:,:]
for i in np.arange(len(swe)): ## loop over year
	for j in np.arange(len(lats)): ## loop over latitude
		for k in np.arange(len(lons)): ## loop over longitude
			### don't calculate area for missing value elements
                        if (math.isnan(swe[i,j,k])) == False:
				if_in_box = mask_latlon(lats[j],lons[k],basin)
				adjust_mask = lat_lon_adjust(lats[j],lons[k],basin)
				mean_swe = historical_sum_swe(lats[j],lons[k]) 
				## new historical swe function based on livneh instead of vic simulations 
				if if_in_box and adjust_mask and mean_swe:
					ind = i*12
					pet_agg.append(np.sum(petnat[ind:ind+11,j,k]) + np.sum(petshort[ind:ind+11,j,k]) + np.sum(pettall[ind:ind+11,j,k]))
					aet_agg.append(np.sum(evap[ind:ind+11,j,k]) + np.sum(transp[ind:ind+11,j,k])) 
					lats_inc.append(lats[j])
					lons_inc.append(lons[k])

### save arrays to files 
filearrayname = '/raid9/gergel/agg_snowpack/%s/moistdef_%s.npz' %(scenario,basin) 
np.savez(filearrayname,lats=np.asarray(lats_inc),lons=np.asarray(lons_inc),pet=np.asarray(pet_agg),aet=np.asarray(aet))
print("finished analysis for %s %s" %(scenario,basin)) 			 





