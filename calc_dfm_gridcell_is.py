
# coding: utf-8

# In[25]:

import numpy as np
import xray
# from xray import ufuncs
import os
import math 
import gc 
import pandas as pd 
from snowpack_functions import get_elev_for_lat_lon,import_gridcell_elevation
import datetime as dt
import sys

# IMPORT DATA FROM INTEGRATED SCENARIOS ARCHIVE 

# In[26]:

################################# INPUTS #############################
args = sys.argv[1:]
model = args[0]
scenario = args[1]
lat = np.float(args[2])
lon = np.float(args[3])

#lat = 48.03125
#model = "CNRM-CM5"
#scenario="historical"
#lat = 48.021
#lon = -121.28125
#lon = -121.25
######################################################################

direc = '/raid/gergel/%s' % "tmin"
tmin_file = "%s_%s_%s.nc" % (model,scenario,"tasmin")
tmin_full = xray.open_dataset(os.path.join(direc,tmin_file)) ## load tmin

direc = '/raid/gergel/%s' % "tmax"
tmax_file = "%s_%s_%s.nc" % (model,scenario,"tasmax")
tmax_full = xray.open_dataset(os.path.join(direc,tmax_file)) ## load tmax

direc = '/raid/gergel/%s' % "rh"
q_file = "%s_%s_%s.nc" % (model,scenario,"huss")
q_full = xray.open_dataset(os.path.join(direc,q_file)) ## load specific humidity

direc = '/raid/gergel/%s' % "precip"
pr_file = "%s_%s_%s.nc" % (model,scenario,"pr")
pr_full = xray.open_dataset(os.path.join(direc,pr_file)) ## load precip

## adjust lat/lon dimensions since the index names are different
tmin_lons_new = tmin_full['lon'].values[tmin_full['lon'].values > 180] - 360 
tmin_full['lon'] = tmin_lons_new
tmax_full['lon'] = tmin_lons_new
pr_full['lon'] = tmin_lons_new
q_full['lon'] = tmin_lons_new 

## select out gridcell 
lon_ind = np.argmin(np.abs(pr_full.lon - lon))
lat_ind = np.argmin(np.abs(pr_full.lat - lat))

## get julian days 
julians = pd.DatetimeIndex(np.asarray(pr_full.time)).dayofyear

tmin = tmin_full.isel_points(lon=[lon_ind],lat=[lat_ind])['air_temp_min'].values[0,:] ## air_temp_min
tmax = tmax_full.isel_points(lon=[lon_ind],lat=[lat_ind])['air_temp_max'].values[0,:] ## air_temp_max
q = q_full.isel_points(lon=[lon_ind],lat=[lat_ind])['specific_humidity'].values[0,:] ## specific_humidity
# pptamt = pr_full.isel_points(lon=[lon_ind],lat=[lat_ind]) ## variable is precipitation 
pptamt = pr_full.isel_points(lon=[lon_ind],lat=[lat_ind])['precipitation'].values[0,:]  ## variable is precipitation 

del tmax_full, q_full,pr_full
gc.collect() 


# 100-hr and 1000-hr DFM FUNCTION 

# In[27]:

def calc_fm100_fm1000(pptdur,maxrh,minrh,maxt,mint,lat,tmois,bv,julians,ymc100): 
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
    if julians > 365:
        julians = 365
    phi = lat * 0.01745 ## converts latitude to radians
    decl = .41008*np.sin((julians-82)*0.01745)
    daylit = 24.0*(1-np.arccos(np.tan(phi)*np.tan(decl))/3.14159)
    daylit = daylit.real
    
    #emc1 = np.ndarray(shape=(len(maxrh)),dtype='float')
    if minrh <= 10:
        emc1= 0.03229 + (0.281073 * minrh) - (0.000578 * minrh * maxt)
    elif minrh > 10 and minrh <= 50: 
        emc1 = 2.22749 + (0.160107 * minrh) - (0.014784 * maxt)
    else: 
        emc1 = 21.0606 + (0.005565 * (minrh**2)) - (0.00035 * minrh * maxt) - (0.483199 * minrh)

    #emc2 = np.ndarray(shape=(len(maxrh)),dtype='float')
    if maxrh <= 10:
        emc2 = 0.03229 + (0.281073 * maxrh) - (0.000578 * maxrh* mint)
    elif maxrh > 10 and maxrh <= 50: 
        emc2 = 2.22749 + (0.160107 * maxrh) - (0.014784 * mint)
    else: 
        emc2 = 21.0606 + (0.005565 * (maxrh**2)) - (0.00035 * maxrh * mint) - (0.483199 * maxrh)
    
    ## qc maxrh 
    # for day in np.arange(len(emc1)):
    if np.isnan(maxrh):
        emc1 = np.nan
        emc2 = np.nan 

    emc = (daylit * emc1 + (24.0 - daylit) * emc2) / 24.0 

    ## qc precip duration 
    # for day in np.arange(len(pptdur)):
    
    # pptdur = pptdur*1.25
    
    if pptdur < 0:
        pptdur = 0
    elif pptdur > 8:
        pptdur = 8
       
    bndry1 = ((24.0 - pptdur) * emc + (0.5 * pptdur + 41) * pptdur) / 24.0 
    fm100 = ((bndry1 - ymc100) * fr100) + ymc100 
    ## calculate 1000-hr fuel moisture daily using average of boundary conditions for
    ## past seven days. starting value set by climate type. 

    fr1 = 0.3068

    bvave = 0

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


# IMPORT BETA VALUES AND APPLY EMPIRICAL TRANSFORM 

# In[28]:

direc = '/raid/gergel'
pdur_file = 'pduration.nc'
pdur_full = xray.open_dataset(os.path.join(direc,pdur_file)) ## pdur beta parameter for John's transform from Matt Jolly
## select out gridcell for pdur b parameter
lon_ind_1 = np.argmin(np.abs(pdur_full.lon - lon))
lat_ind_1 = np.argmin(np.abs(pdur_full.lat - lat))
beta = pdur_full.isel_points(lon=[lon_ind_1],lat=[lat_ind_1])['pdur'].values

# pptamt_in = pptamt * 0.04 ## convert from mm to inches 
pptamt_in = pptamt * 0.04
# pptdur_calc_df = pptamt_in['precipitation'].to_series().map(lambda x: np.round(24 * (1 - (np.exp(-beta['pdur']*x)))) if (x > 0) else 0) 
pptdur = np.round(24 * (1 - (np.exp(-beta * pptamt_in))))

# pptdur = xray.DataArray.from_series(pptdur_calc_df).to_dataset()['precipitation'].values[0,:]


# ITERATE AND CALCULATE 100-HR AND 1000-HR DFM WITH DERIVED RELATIVE HUMIDITY (FROM SPECIFIC HUMIDITY) 

# In[30]:

## get elevation of grid cell
soil_file = '/raid9/gergel/agg_snowpack/soil_avail.txt'
elev_corr_info = import_gridcell_elevation(soil_file) 
print(np.round(tmin_full.lat[lat_ind],decimals=5))
print(tmin_full.lon[lon_ind]) 

h = get_elev_for_lat_lon(elev_corr_info,np.round(tmin_full.lat[lat_ind],decimals=5),np.round(tmin_full.lon[lon_ind],decimals=5))

## get pressure 
p = estimate_p(h)

x = 1

tmois=np.zeros(shape=(x,7))
bv=np.zeros(shape=(x,7))
ymc=np.zeros(shape=(x,1))
ndays = len(q)

fm1000_rh = np.ndarray(shape=(x,ndays),dtype='float')
fm100_rh = np.ndarray(shape=(x,ndays),dtype='float')

for day in np.arange(ndays):
    t_avg = (tmax[day] + tmin[day])/2.0 ## in Kelvin still 
    e_s = estimate__e_s(t_avg) ## sat vapor pressure
    satvpx = estimate__e_s(tmax[day])
    satvpn = estimate__e_s(tmin[day])
    RH = estimate_relative_humidity(q[day],e_s,p)
    ambvp = (RH * e_s) / 100.0 
    rhmax = 100.0 * (ambvp/satvpn)
    ## constrain RH to be 100% or less 
    if rhmax > 100:
        rhmax = 100
    rhmin = 100.0 * (ambvp/satvpx)
    if rhmin > 100:
        rhmin = 100

    tmois,fm1000_rh[0,day],fm100_rh[0,day],bv = calc_fm100_fm1000(np.float(pptdur[day]),rhmax,rhmin,np.float(kelvin_to_fahrenheit(tmax[day])),np.float(kelvin_to_fahrenheit(tmin[day])),np.float(tmin_full.lat[lat_ind]),tmois,bv,julians[day],ymc)
    
    ymc=fm100_rh[0,day]


# CREATE ARRAY FOR DATAFRAME INDEX 

# In[32]:

if (scenario == "historical"):
    tp_start = dt.datetime(1950,1,1)
    tp_end = dt.datetime(2006,1,1)
else:
    tp_start = dt.datetime(2006,1,1)
    tp_end = dt.datetime(2100,1,1)

dates = [tp_start + dt.timedelta(days=i) for i in range(0, (tp_end - tp_start).days)]
dates_arr = np.asarray(dates)


# WRITE TO NETCDF FILE

# In[37]:

d = {'fm100':fm100_rh[0,:],'fm1000':fm1000_rh[0,:]}
df = pd.DataFrame(data={'fm100':fm100_rh[0,:],'fm1000':fm1000_rh[0,:],'lat':np.asarray(np.round(tmin_full.lat[lat_ind],decimals=5)),'lon':np.asarray(np.round(tmin_full.lon[lon_ind],decimals=5))},index=dates_arr)
ds = xray.Dataset.from_dataframe(df)
direc = '/raid/gergel/dfm_results/%s/%s' % (model,scenario)
if not os.path.exists(direc):
    os.makedirs(direc) ## if directory doesn't exist, create it 
## save to netcdf 
filename = 'dfm_%s_%s.nc' % (str(lat),str(lon))
ds.to_netcdf(os.path.join(direc,filename))
print("saved netcdf to %s" % os.path.join(direc,filename)) 

# In[ ]:




# In[ ]:



