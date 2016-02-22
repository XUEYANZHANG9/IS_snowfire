import numpy as np
import xray
from xarray import ufuncs
import os
import math
import gc
import pandas as pd
import datetime as dt
import sys
import operator

sys.stdout.flush()

# INPUTS
args = sys.argv[1:]
model = args[0]
scenario = args[1]

# model = "CNRM-CM5"
# scenario="historical"
chunk_number = 1200
direc = '/raid/gergel/%s' % "tmin"
tmin_file = "%s_%s_%s.nc" % (model, scenario, "tasmin")
tmin_f = xray.open_dataset(os.path.join(direc, tmin_file), chunks={'time': chunk_number}) #  load tmin

direc = '/raid/gergel/%s' % "tmax"
tmax_file = "%s_%s_%s.nc" % (model, scenario, "tasmax")
tmax_f = xray.open_dataset(os.path.join(direc, tmax_file), chunks={'time': chunk_number}) #  load tmax

direc = '/raid/gergel/%s' % "rh"
q_file = "%s_%s_%s.nc" % (model, scenario, "huss")
q_f = xray.open_dataset(os.path.join(direc, q_file), chunks={'time': chunk_number}) #  load specific humidity

direc = '/raid/gergel/pptdur'
pr_file = "%s_%s.nc" % (model, scenario)
pptdur = xray.open_dataset(os.path.join(direc, pr_file), chunks={'time': chunk_number}) #  load precip

# adjust lat/lon dimensions since the index names are different
tmin_lons_new = tmin_f['lon'].values[tmin_f['lon'].values > 180] - 360
tmin_f['lon'] = tmin_lons_new
tmax_f['lon'] = tmin_lons_new
q_f['lon'] = tmin_lons_new

# cut out conus east of 103 for each variable
swe_mask_file = '/raid9/gergel/agg_snowpack/goodleap/SWE/histmeanmask.nc' #  1s are swe, 0s are no swe
swe_mask = xray.open_dataset(swe_mask_file)
# rename dimensions
swe_mask.rename({"Latitude": "lat", "Longitude": "lon", "Time": "time"}, inplace=True)
swe_mask = swe_mask.squeeze()

def slice_dataset(ds_array, ds_to_slice): 
	'''
	slices second Dataset to fit first Dataset
	'''
	swe_mask_align, array_align = xray.align(ds_array, ds_to_slice, join='inner', copy=False)
	return(array_align)


# Dataset join
tmax = slice_dataset(swe_mask, tmax_f)
tmin = slice_dataset(swe_mask, tmin_f)
q = slice_dataset(swe_mask,q_f)

# get julian days
julians = pd.DatetimeIndex(np.asarray(tmin.time)).dayofyear

# 100-hr and 1000-hr DFM FUNCTION

def constrain_dataset(da,bool_operator,constrain_value,fill_value):
	''' 
	constrains masked values of dataset to be above/below given value,fills with given value and accounts for possible existing nans 
	'''
    	import operator
    	import xray
    	da = da.fillna(-9999)
    	da = da.where((bool_operator(da, constrain_value )) & ( da == -9999)).fillna( fill_value)
    	da = da.where(da != -9999).fillna(np.nan)
    	return(da)

def calc_fm100_fm1000(x, pptdur, maxrh, minrh, maxt, mint, lat, tmois, bv, julians, ymc100):
    	'''
	compute the average boundary conditions for the past
    	24 hour and 100-hr-tl fuel moisture. The boundary conditions are weighted averages
    	of the EQMCs calculated from the temp and RH values. Philat is used to calculate
    	daylength which is the basis of the weighting function.
	'''
    	fr100 = 0.3156

    	sys.stdout.flush()

    	# John's calcDaylight function
    	if julians > 365:
		julians = 365

    	phi = lat * 0.01745  # converts latitude to radians
    	decl = .41008*np.sin((julians-82)*0.01745)
    	daylit = 24.0*(1-np.arccos(np.tan(phi)*np.tan(decl))/3.14159)
    	daylit = daylit.real
	
	minrh_sq = ufuncs.square(minrh)
    	minrh = minrh.values
	maxt = maxt.values
	mint = mint.values
    	inds = np.nonzero(minrh.data <= 10)
    	minrh[inds] = 0.03229 + (0.281073 * minrh[inds]) - (0.000578 * minrh[inds] * maxt[inds])
    	inds = np.nonzero((minrh > 10) & (minrh <= 50))
    	minrh[inds] = 2.22749 + (0.160107 * minrh[inds]) - (0.014784 * maxt[inds])
    	inds = np.nonzero(minrh > 50)
    	minrh[inds] = 21.0606 + (0.005565 * (minrh_sq.values[inds])) - (0.00035 * minrh[inds] * maxt[inds]) - (0.483199 * minrh[inds])
	emc1 = minrh

	maxrh_sq = ufuncs.square(maxrh) 
    	maxrh = maxrh.values 
    	inds = np.nonzero(maxrh <= 10)
    	maxrh[inds] = 0.03229 + (0.281073 * maxrh[inds]) - (0.000578 * maxrh[inds] * mint[inds])
    	inds = np.nonzero((maxrh > 10) & (maxrh <= 50))
    	maxrh[inds] = 2.22749 + (0.160107 * maxrh[inds]) - (0.014784 * mint[inds])
    	inds = np.nonzero((maxrh > 50) & (maxrh <= 80)) 
    	maxrh[inds] = 21.0606 + (0.005565 * (maxrh_sq.values[inds])) - (0.00035 * maxrh[inds] * mint[inds]) - (0.483199 * maxrh[inds])
	inds = np.nonzero(maxrh > 50) 
        maxrh[inds] = 21.0606 + (0.005565 * (maxrh_sq.values[inds])) - (0.00035 * maxrh[inds] * mint[inds]) - (0.483199 * maxrh[inds])
	emc2 = maxrh

    	print("calculated emc2")

	def emc1(rh,t):
		if rh < 10:
        		emc = 0.03229 + (0.281073 * rh) - (0.000578 * rh * t)
			return(emc) 
		else:
			return(rh)  

    	emc = (daylit.reshape(maxrh.shape) * emc1 + (24.0 - daylit.reshape(maxrh.shape)) * emc2) / 24.0

    	print("calculated emcs")

    	# qc precip duration
    	pptdur = constrain_dataset(pptdur, operator.le, 8, 8)
    	pptdur = constrain_dataset(pptdur, operator.gt, 0, 0)

    	bndry1 = ((24.0 - pptdur) * emc + (0.5 * pptdur + 41) * pptdur) / 24.0
    	fm100 = ((bndry1 - ymc100) * fr100) + ymc100

    	# calculate 1000-hr fuel moisture daily using average of boundary conditions for past seven days. starting value set by climate type.
    	fr1 = 0.3068

    	# accumulate a 6-day total
	bv = np.roll(bv, -1, axis=0)
	'''
    	bv[0,:,:] = bv[1,:,:]
    	bv[1,:,:] = bv[2,:,:]
    	bv[2,:,:] = bv[3,:,:]
    	bv[3,:,:] = bv[4,:,:]
    	bv[4,:,:] = bv[5,:,:]
    	bv[5,:,:] = bv[6,:,:]
	'''

    	bvave = bv.sum(axis=1)

    	bndry = ((24 - pptdur) * emc + (2.7 * pptdur + 76) * pptdur) / 24.0
    	bv[6,:,:] = bndry


    	# add today's boundary from subfm100, divide by 7 days
    	bvave = (bvave + bndry) / 7.0

    	# calculate today's 1000 hr fuel moisture
    	fm1000 = tmois[0, :, :] + (bvave - tmois[0, :, :]) * fr1

    	# move each days 1000 hr down one, drop the oldest
    	tmois = np.roll(tmois, -1, axis=0)
	'''
    	tmois[0,:,:] = tmois[1,:,:]
    	tmois[1,:,:] = tmois[2,:,:]
    	tmois[2,:,:] = tmois[3,:,:]
    	tmois[3,:,:] = tmois[4,:,:]
    	tmois[4,:,:] = tmois[5,:,:]
    	tmois[5,:,:] = tmois[6,:,:]
	'''
    	
	tmois[6,:,:] = fm1000

    	return(tmois,fm1000,fm100,bv)

def kelvin_to_fahrenheit(T):
	''' 
	converts T in Kelvin to Fahrenheit
	'''
    	F = ((9.0 / 5.0) * (T - 273.15)) + 32.0
    	return (F)

def estimate_p(h):
	''' 
	calculates pressure based on elevation
	'''
    	p = 101325 * (1 - ((2.25577 * 10 ** -5) * h)) ** 5.25588  # Pascals
    	return (p)

def estimate__e_s(T):
    	''' 
	estimates saturation vapor pressure
	'''
    	T0 = 273.15 #  Kelvin, reference temperature
    	e_s = 611 * ufuncs.exp(( 17.67 * (T - T0)) / (T - 29.65) )
    	return (e_s)

def estimate_relative_humidity(q, e_s, p):
    	'''
	estimates relative humidity using hypsometric equation for \n 
	pressure, virtual temperature and avg temperature
	'''
    	w = q  # approximating the mixing ratio as the specific humidity
    	w_s = 0.622 * (e_s / p)
    	RH = 100.0 * (w / w_s)
    	return (RH)

x = len(q.lat) * len(q.lon)  # number of grid cells
nlat = len(q.lat)
nlon = len(q.lon)

# get gridcell elevations
h = np.zeros((nlat, nlon))

# get list of lats for each day
lons_grid,lats_grid = np.meshgrid(q.lon,q.lat)
lats = lats_grid.flatten()

# get pressure
p = estimate_p(h)

tmois = np.zeros(shape=(7, nlat, nlon))
bv = np.zeros(shape=(7, nlat, nlon))
ymc = np.zeros(shape=(nlat, nlon))
ndays = len(julians)

# INITIALIZE DFM ARRAYS TO FILL IN OVER ITERATION
fm1000_rh = np.ndarray(shape=(ndays, nlat, nlon), dtype='float')
fm100_rh = np.ndarray(shape=(ndays, nlat, nlon),  dtype='float')

# ITERATE AND CALCULATE 100 HR AND 1000 HR DFM
for day in xrange(ndays):
	print("now calculating day %f" % day)
	t_avg = ((tmax['air_temp_max'].isel(
					time=day) + tmin['air_temp_min'].isel(time=day)) / 2.0)
	e_s = estimate__e_s(t_avg)  # saturation vapor pressure
	satvpx = estimate__e_s(tmax.isel(time=day))
	satvpn = estimate__e_s(tmin.isel(time=day))
	RH = estimate_relative_humidity(q.isel(time=day), e_s, p)
	ambvp = (RH * e_s) / 100.0
	rhmax = 100.0 * (ambvp['specific_humidity'] / satvpn['air_temp_min'])
	rhmin = 100.0 * (ambvp['specific_humidity'] / satvpx['air_temp_max'])
	'''
	# constrain RH to be 100 % or less
        rhmin = constrain_dataset(rhmin, operator.le, 100, 100)
	rhmax = constrain_dataset(rhmax, operator.le, 100, 100)
	'''
	tmois, fm1000_rh[day, :, :], fm100_rh[day, :, :], bv = calc_fm100_fm1000(
										x, pptdur.isel(time=day), rhmax, rhmin,
										kelvin_to_fahrenheit(tmax['air_temp_max'].isel(time=day)),
										kelvin_to_fahrenheit(tmin['air_temp_min'].isel(time=day)),
										lats, tmois, bv, julians[day], ymc
										)

	ymc = fm100_rh[day, :, :]
	print(day)

print("finished iteration loop")

# CONSTRUCT DATASET

ds = xray.Dataset()
lon_da = xray.DataArray(
			tmax.lon, dims=('longitude', ), name='longitude',
			attrs={'long_name': 'longitude coordinate'})
lat_da = xray.DataArray(
			tmax.lat, dims=('latitude', ), name='latitude',
			attrs={'long_name': 'latitude coordinate'})
ds['fm100'] = xray.DataArray(
			fm100_rh, dims=('latitude', 'longitude'), name='fm100',
			coords={'latitude': lat_da, 'longitude': lon_da},
			attrs={'long_name': '100 hr dead fuel moisture'})
ds['fm1000'] = xray.DataArray(
			fm1000_rh, dims=('latitude', 'longitude'), name='fm1000',
			coords={'latitude': lat_da, 'longitude': lon_da},
			attrs={'long_name': '1000 hr dead fuel moisture'})
ds['time'] = xray.DataArray(
			tmax.time, dims=('latitude', 'longitude'), name='time',
			coords={'latitude': lat_da, 'longitude': lon_da},
			attrs={'long_name': 'time'})

# WRITE TO NETCDF
direc = '/raid/gergel/dfm' % (model, scenario)
if not os.path.exists(direc):
	os.makedirs(direc)  # if directory doesn't exist, create it
# save to netcdf
filename = '%s_%s.nc' % (model, scenario)
ds.to_netcdf(os.path.join(direc, filename))
print("saved netcdf to %s " % os.path.join(direc, filename))
