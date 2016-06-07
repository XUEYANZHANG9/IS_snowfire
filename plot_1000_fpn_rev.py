# coding: utf-8

import matplotlib
matplotlib.use('Agg')
import xarray as xray
import os
import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
from dfm_functions import make_map, make_mask, cmap_discretize 

# In[49]:

direc = '/raid/gergel/dfm/hist'
model = "CCSM4"
scenario = "historical"
chunk = "1970_1999"
filename = '%s_%s_%s.nc' % (model, scenario, chunk)
ds = xray.open_dataset(os.path.join(direc,filename))
u = ds['fm1000'].groupby('time.month').mean('time')
# average of JAS months 
v = (u.sel(month=7) + u.sel(month=8) + u.sel(month=9)) / 3.0

# mask domain
mask_domain_mtns = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/mountains', ds.lat, ds.lon)
mask_domain_lowlands = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/lowlands', ds.lat, ds.lon)

fs = 15 ## fontsize
nbins = 11
lp = 10
dpi = 300

#f, axes = plt.subplots(nrows=1, ncols=2, figsize=(30,15))
f, axes = plt.subplots(nrows=1, ncols=2, figsize=(6.8,3.4))

direc = '/raid/gergel/dfm/%s' % 'rcp85_2080s'

# average over models 
####################
txt_files = [b for b in os.listdir(direc)]
# txt_files = ['CNRM-CM5_rcp85_2070_2099.nc'] 
################### 

total = 0.0
for ii, f in enumerate(txt_files):
	# load data
	ds = xray.open_dataset(os.path.join(direc,f))
	u = ds['fm1000'].groupby('time.month').mean('time')

	# average of JAS months 
	v_future = (u.sel(month=7) + u.sel(month=8) + u.sel(month=9)) / 3.0

	model = f.split('_')[0]
	filename = '%s_historical_1970_1999.nc' % model 
	
	print(os.path.join('/raid/gergel/dfm/hist', filename))  
	
	ds = xray.open_dataset(os.path.join('/raid/gergel/dfm/hist', filename)) 
	u = ds['fm1000'].groupby('time.month').mean('time') 
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

v.values = fpn_sum 

v_dfm_mtns = v.where(mask_domain_mtns == 1)
v_dfm_low = v.where(mask_domain_lowlands == 1) 

# define min and max for colorbar
vmin=-10
vmax=10 

# discretize colormap
cmap = cmap_discretize(plt.cm.coolwarm_r, 10)

# set fontsize properties
font = {'size' : fs}
plt.rc('font', **font)

# first subplot
ax = axes[0]
plt.sca(ax)
m = make_map(fs, label_parallels=True, label_meridians=True) 
x,y = m(v.lon, v.lat)
img = m.pcolormesh(x, y, v_dfm_mtns.to_masked_array(), cmap=cmap, vmin=vmin, vmax=vmax) 
ax.set_title('Mountains', size=fs)

# second subplot
ax = axes[1]
plt.sca(ax)
m = make_map(fs, label_meridians=True) 
img = m.pcolormesh(x, y, v_dfm_low.to_masked_array(), cmap=cmap, vmin=vmin, vmax=vmax) 
ax.set_title('Lowlands', size=fs)

# get rid of whitespace between subplots
plt.subplots_adjust(wspace=0.1, hspace=None, left=0.05, right=0.98, top=0.9, bottom=0.21)

# create axis for colorbar 
cax = plt.axes([0.04, 0.1, 0.95, 0.05]) #[left,vertical, distance from left, height]

# colorbar and its properties 
cbar = plt.colorbar(img, cax=cax, orientation='horizontal')
cbar.set_ticks([np.linspace(vmin, vmax, 11, endpoint=True, dtype='int')])
cbar.set_label('Model Agreement in 100-hr DFM \n (number positive minus negative)', rotation='horizontal', labelpad=lp)

## save plot
direc = '/raid/gergel/dfm/plots/fm1000'
if not os.path.exists(direc):
    os.makedirs(direc) ## if directory doesn't exist, create it
plotname = 'fpn'
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath, format='tiff', bbox_inches='tight', dpi=dpi)
