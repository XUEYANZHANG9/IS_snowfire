
# coding: utf-8

# In[25]:

import numpy as np
import xray
# from xray import ufuncs
import os
import math 
import gc 
import pandas as pd 
import datetime as dt
import sys

# IMPORT DATA FROM INTEGRATED SCENARIOS ARCHIVE 

# In[26]:

################################# INPUTS #############################
args = sys.argv[1:]
model = args[0]
scenario = args[1]

#model = "CNRM-CM5"
#scenario="historical"

######################################################################

direc = '/raid/gergel/%s' % "tmin"
tmin_file = "%s_%s_%s.nc" % (model,scenario,"tasmin")
tmin_f = xray.open_dataset(os.path.join(direc,tmin_file)) ## load tmin

direc = '/raid/gergel/%s' % "tmax"
tmax_file = "%s_%s_%s.nc" % (model,scenario,"tasmax")
tmax_f = xray.open_dataset(os.path.join(direc,tmax_file)) ## load tmax

direc = '/raid/gergel/%s' % "rh"
q_file = "%s_%s_%s.nc" % (model,scenario,"huss")
q_f = xray.open_dataset(os.path.join(direc,q_file)) ## load specific humidity

direc = '/raid/gergel/pptdur'
pr_file = "%s_%s.nc" % (model,scenario)
pptdur = xray.open_dataset(os.path.join(direc,pr_file)) ## load precip

## adjust lat/lon dimensions since the index names are different
tmin_lons_new = tmin_full['lon'].values[tmin_full['lon'].values > 180] - 360 
tmin_f['lon'] = tmin_lons_new
tmax_f['lon'] = tmin_lons_new
q_f['lon'] = tmin_lons_new 

## cut out conus east of 103 for each variable 
swe_mask_file = '/raid9/gergel/agg_snowpack/goodleap/SWE/histmeanmask.nc' ## 1s are swe, 0s are no swe 
swe_mask = xray.open_dataset(swe_mask_file)
## rename dimensions
swe_mask.rename({"Latitude": "lat", "Longitude": "lon", "Time": "time"}, inplace=True)
swe_mask = swe_mask.squeeze()
## Dataset join 
swe_mask_align,tmax = xray.align(swe_mask,tmax_f,join='inner',copy=False)
swe_mask_align,tmin = xray.align(swe_mask,tmin_f,join='inner',copy=False)
swe_mask_align,q = xray.align(swe_mask,q_f,join='inner',copy=False) 

## get julian days 
julians = pd.DatetimeIndex(np.asarray(tmin.time)).dayofyear

## delete full arrays of each variable for conus 
del tmax_f,tmin_f,q_f,swe_mask,swe_mask_align 
gc.collect() 


# 100-hr and 1000-hr DFM FUNCTION 

# In[27]:

def calc_fm100_fm1000(x,pptdur,maxrh,minrh,maxt,mint,lat,tmois,bv,julians,ymc100): 
    """this subroutine computes the average boundary conditions for the past 
    24 hour and 100-hr-tl fuel moisture. The boundary conditions are weighted averages 
    of the EQMCs calculated from the temp and RH values. Philab is used to calculate 
    daylength which is the basis of the weighting function.""" 

    emc1 = 0
    emc2 = 0
    emc = 0
    bndry1 = 0
    bndry = 0
    bvave = 0
    daylit = 0
    ambvp = 0
    fr100 = 0.3156

    '''# daylit = calcDaylight(j_date,lat) ########## need to write this function 
    #######################
    phi = lat * 0.01745 ## lat is in degrees 
    decl = 0.41008*np.sin(np.deg2rad((julians-82) * 0.01745))
    daylit = 24 * (1.0 - ((np.arccos(np.tan(np.deg2rad(phi)) * np.tan(np.deg2rad(decl))) / math.pi)))'''
    #######################
    
    ## John's calcDaylight function
    for jday in np.arange(len(julians)):
    	if julians[jday] > 365:
        	julians[jday] = 365
    phi = lat * 0.01745 ## converts latitude to radians
    decl = .41008*np.sin((julians-82)*0.01745)
    daylit = 24.0*(1-np.arccos(np.tan(phi)*np.tan(decl))/3.14159)
    daylit = daylit.real
    
    emc1 = np.ndarray(shape=x),dtype='float')
    for gc in np.arange(len(lat)):
    	if minrh[gc] <= 10:
        	emc1[gc]= 0.03229 + (0.281073 * minrh[gc]) - (0.000578 * minrh[gc] * maxt[gc])
    	elif minrh[gc] > 10 and minrh[gc] <= 50: 
        	emc1[gc] = 2.22749 + (0.160107 * minrh[gc]) - (0.014784 * maxt[gc])
    	else: 
        	emc1[gc] = 21.0606 + (0.005565 * (minrh[gc]**2)) - (0.00035 * minrh[gc] * maxt[gc]) - (0.483199 * minrh[gc])

    emc2 = np.ndarray((shape=x),dtype='float')
    for gc in np.arange(len(lat)):
    	if maxrh[gc] <= 10:
        	emc2[gc] = 0.03229 + (0.281073 * maxrh[gc]) - (0.000578 * maxrh[gc]* mint[gc])
    	elif maxrh > 10 and maxrh <= 50: 
        	emc2[gc] = 2.22749 + (0.160107 * maxrh[gc]) - (0.014784 * mint[gc])
    	else: 
        	emc2[gc] = 21.0606 + (0.005565 * (maxrh[gc]**2)) - (0.00035 * maxrh[gc] * mint[gc]) - (0.483199 * maxrh[gc])
    
    ## qc maxrh 
    for gc in np.arange(len(emc1[:,0])):
    	if np.isnan(maxrh[gc]):
        	emc1[gc] = np.nan
        	emc2[gc] = np.nan 

    emc = (daylit * emc1 + (24.0 - daylit) * emc2) / 24.0 

    ## qc precip duration 
    # for day in np.arange(len(pptdur)):
    
    # pptdur = pptdur*1.25
    
    for gc in np.arange(len(pptdur)):
    	if pptdur[gc] < 0:
        	pptdur[gc] = 0
    	elif pptdur[gc] > 8:
        	pptdur[gc] = 8
       
    bndry1 = ((24.0 - pptdur) * emc + (0.5 * pptdur + 41) * pptdur) / 24.0 
    fm100 = ((bndry1 - ymc100) * fr100) + ymc100 
    ## calculate 1000-hr fuel moisture daily using average of boundary conditions for
    ## past seven days. starting value set by climate type. 

    fr1 = 0.3068

    bvave = np.zeros(x)

    ## accumulate a 6-day total
    for i in np.arange(0,6):
        bv[:,i] = bv[:,i+1]
        bvave = bvave + bv[:,i]

    bndry = ((24 - pptdur) * emc + (2.7 * pptdur + 76) * pptdur) / 24.0 
    bv[:,6] = bndry

    ## add today's boundary from subfm100, divide by 7 days 
    bvave = (bvave + bndry) / 7.0 

    ## calculate today's 1000 hr fuel moisture 
    # fm1000 = tmois[:,1] + (bvave - tmois[:,1])*fr1 
    fm1000 = tmois[:,0] + (bvave - tmois[:,0])*fr1

    ## move each days 1000 hr down one, drop the oldest 
    for i in np.arange(0,6):
        tmois[:,i] = tmois[:,i+1] 
    tmois[:,6] = fm1000 

    return(tmois,fm1000,fm100,bv)

def kelvin_to_fahrenheit(T):
    ''' converts T in Kelvin to Fahrenheit'''
    F = ((9.0/5.0) * (T - 273.15)) + 32.0
    return(F)

def estimate_p(h):
    p = 101325 * (1 - ((2.25577 * 10**-5) * h))**5.25588 ## Pascals 
    return(p)

def estimate__e_s(T): 
    ''' estimates saturation vapor pressure'''
    T0 = 273.15 ## Kelvin, reference temperature
    e_s = 611 * np.exp((17.67 * (T - T0)) / (T - 29.65) )
    return(e_s)

def estimate_relative_humidity(q,e_s,p):
    '''estimates relative humidity using hypsometric equation for pressure, virtual temperature and avg temperature'''
    import numpy as np
    w = q ## approximating the mixing ratio as the specific humidity
    w_s = 0.622 * (e_s / p)
    RH = 100.0 * (w / w_s)
    return (RH)


###################################################################################################### 

x = len(q.lat*q.lon) ## number of grid cells 

## get gridcell elevations 
h = np.zeros(x) 

## get pressure
p = estimate_p(h)

tmois=np.zeros(shape=(x,7))
bv=np.zeros(shape=(x,7))
ymc=np.zeros(shape=(x,1))
ndays = len(q.time)

## INITIALIZE DFM ARRAYS TO FILL IN OVER ITERATION 
fm1000_rh = np.ndarray(shape=(x,ndays),dtype='float')
fm100_rh = np.ndarray(shape=(x,ndays),dtype='float')

t_avg = (tmax['air_temperature_max'] + tmin['air_temperature_min']) / 2.0 ## in kelvin still
e_s = estimate__e_s(t_avg) ## saturation vapor pressure 
satvpx = estimate__e_s(tmax['air_temp_max'])
satvpn = estimate__e_s(tmin['air_temp_min']) 
RH = estimate_relative_humidity(q['specific_humidity'],e_s,p) 
ambvp = (RH * e_s) / 100.0 
rhmax = 100.0 * (ambvp / satvpn) 
rhmin = 100.0 * (ambvp / satvpn) 
## constrain RH to be 100 % or less

def constrain_rh(RH):
	''' this function constrains relative humidity to be equal or less than 100 %'''
	if RH > 100: 
		RH = 100
	return(RH) 

rhmax.apply(constrain_rh,keep_attrs=True) 
rhmin.apply(constrain_rh,keep_attrs=True) 

# ITERATE AND CALCULATE 100 HR AND 1000 HR DFM 
for day in np.arange(ndays):
	tmois,fm1000_rh[:,day],fm100_rh[:,day],bv = calc_fm100_fm1000(x,pptdur,rhmax,rhmin,kelvin_to_fahrenheit(tmax['air_temp_max']),kelvin_to_fahrenheit(tmin['air_temp_min']),tmin_full.lat,tmois,bv,julians,ymc)
    
	ymc=fm100_rh[:,day]

# CONSTRUCT DATASET

ds = xray.Dataset() 
lon_da = xray.DataArray(tmax.lon,dims=('longitude', ), name='longitude', attrs={'long_name': 'longitude coordinate'}) 
lat_da = xray.DataArray(tmax.lat,dims=('latitude', ), name='latitude', attrs={'long_name': 'latitude coordinate'}) 
ds['fm100'] = xray.DataArray(fm100_rh, dims=('latitude','longitude'), name='fm100', coords={'latitude': lat_da, 'longitude': lon_da},attrs={'long_name': '100 hr dead fuel moisture'}) 
ds['fm1000'] = xray.DataArray(fm1000_rh, dims=('latitude','longitude'), name='fm1000', coords={'latitude': lat_da, 'longitude': lon_da},attrs={'long_name': '1000 hr dead fuel moisture'})
ds['time'] = xray.DataArray(tmax.time,dims=('latitude','longitude'), name='time', coords={'latitude': lat_da, 'longitude': lon_da},attrs={'long_name': 'time'})

## WRITE TO NETCDF 
direc = '/raid/gergel/dfm' % (model,scenario)
if not os.path.exists(direc):
    os.makedirs(direc) ## if directory doesn't exist, create it 
## save to netcdf 
filename = '%s_%s.nc' %(model,scenario)  
ds.to_netcdf(os.path.join(direc,filename))
print("saved netcdf to %s" % os.path.join(direc,filename)) 





