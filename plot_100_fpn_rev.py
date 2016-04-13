# coding: utf-8

import matplotlib
matplotlib.use('Agg')
import xarray as xray
import os
import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
from dfm_functions import make_map 

# In[49]:

direc = '/raid/gergel/dfm/hist'
model = "CCSM4"
scenario = "historical"
chunk = "1970_1999"
filename = '%s_%s_%s.nc' % (model, scenario, chunk)
ds = xray.open_dataset(os.path.join(direc,filename))
u = ds['fm100'].groupby('time.month').mean('time')
# average of JAS months 
v = (u.sel(month=7) + u.sel(month=8) + u.sel(month=9)) / 3.0

def unit_test_mask_domain(lats, lons, mask, num_gridcells):
    if len(lats) != len(lons):
        raise ValueError('Length of lats not equal to length of lons')
    if (num_gridcells != len(lats)):
        raise ValueError('Length of points not equal to the number of gridcells in domain')


# In[51]:

def make_mask(direc, ds_lat, ds_lng):
    # create list of files 
    txt_files = [i for i in os.listdir(direc)]
    count_gridcells = 0

    # create list of full lats/lons in domain
    for i, f in enumerate(txt_files):
        with open(os.path.join(direc,f)) as file_object:
            data = pd.read_csv(file_object)
            lats = data['lat_%s' % f.split('.')[0]]
            lons = data['lon_%s' % f.split('.')[0]]
            if i == 0:
                lats_full = lats
                lons_full = lons
                count_gridcells = len(lats)
            else:
                lats_full = pd.concat([lats_full, lats])
                lons_full = pd.concat([lons_full, lons])
                count_gridcells += len(lats)

    # create set for set query 
    s = {(l1,l2) for l1,l2 in zip(lats_full,lons_full)}

    # initialize mask array for entire domain
    mask_domain = np.zeros(shape=(len(ds_lat),len(ds_lng)))

    # create mask for the region 
    for j, l1 in enumerate(np.asarray(ds_lat)):
        for k, l2 in enumerate(np.asarray(ds_lng)):
            if (l1,l2) in s:
                mask_domain[j,k] = 1

    # test that mask is correct using unit test 
    unit_test_mask_domain(lats_full, lons_full, mask_domain, count_gridcells)
    return(mask_domain)

# mask domain
mask_domain_mtns = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/mountains', ds.lat, ds.lon)
mask_domain_lowlands = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/lowlands', ds.lat, ds.lon)

fs = 30 ## fontsize
nbins = 11
lp = 20

f, axes = plt.subplots(nrows=1, ncols=2, figsize=(20,6))

direc = '/raid/gergel/dfm/%s' % 'rcp85_2080s'

# average over models 
txt_files = [b for b in os.listdir(direc)]

total = 0.0
for ii, f in enumerate(txt_files):
	# load data
	ds = xray.open_dataset(os.path.join(direc,f))
	u = ds['fm100'].groupby('time.month').mean('time')

	# average of JAS months 
	v_future = (u.sel(month=7) + u.sel(month=8) + u.sel(month=9)) / 3.0

	model = f.split('_')[0]
	filename = '%s_historical_1970_1999.nc' % model 
	
	print(os.path.join('/raid/gergel/dfm/hist', filename))  
	
	ds = xray.open_dataset(os.path.join('/raid/gergel/dfm/hist', filename)) 
	u = ds['fm100'].groupby('time.month').mean('time') 
	v_hist = (u.sel(month=7) + u.sel(month=8) + u.sel(month=9)) / 3.0 
	
	v = v_future - v_hist 

        # prepare data for FP/FN figure 
	v_vals = v.values

        v_vals[v_vals < 0] = -1.00
	v_vals[v_vals > 0] = 1.00 

        if ii == 0:
        	fpn_sum = v_vals
        else:
        	fpn_sum += v_vals

        total += 1.00

print(total) 
fpn = fpn_sum / total 
 
v.values = fpn * 100 # convert to percent 

v_dfm_mtns = v.where(mask_domain_mtns == 1)
v_dfm_low = v.where(mask_domain_lowlands == 1) 

vmin=-100
vmax=100 

ax = axes[0]
plt.sca(ax)

m = make_map(fs, label_parallels=True, label_meridians=True) 

x,y = map(v.lon, v.lat)

# img = v_dfm_mtns.plot(ax=ax, vmin=vmin, vmax=vmax, cmap='bwr_r', add_labels=False, add_colorbar=False)
img = m.pcolormesh(x, y, v_dfm_mtns.to_masked_array(), cmap='bwr_r', vmin=vmin, vmax=vmax) 
cbar = plt.colorbar(img)
cbar.set_ticks([np.linspace(vmin, vmax, 6, endpoint=True, dtype='int')])
#cbar.set_ticks([-100, 50, 0, 50, 100])
cbar.set_label('FPN \n (%)',
                        rotation='horizontal', labelpad=lp)
ax.set_title('Mountains')
ax.set_xlabel('Longitude', labelpad=lp) 
ax.set_ylabel('Latitude', labelpad=lp) 
font = {'size' : fs}
plt.rc('font', **font)

ax = axes[1]
plt.sca(ax)

m = make_map(fs, label_meridians=True) 

# img = v_dfm_low.plot(ax=ax, vmin=vmin, vmax=vmax, cmap='bwr_r', add_labels=False, add_colorbar=False)
img = m.pcolormesh(x, y, v_dfm_low.to_masked_array(), cmap='bwr_r', vmin=vmin, vmax=vmax) 
cbar = plt.colorbar(img)
cbar.set_ticks([np.linspace(-100, 100, 6, endpoint=True, dtype='int')])
#cbar.set_ticks([-100, 50, 0, 50, 100])
cbar.set_label('FPN \n (%)',         
                        rotation='horizontal', labelpad=lp)
ax.set_title('Lowlands')
ax.set_xlabel('Longitude', labelpad=lp)
font = {'size' : fs}
plt.rc('font', **font)

## save plot
direc = '/raid/gergel/dfm/plots/fm100'
if not os.path.exists(direc):
    os.makedirs(direc) ## if directory doesn't exist, create it
plotname = 'fpn'
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath)
