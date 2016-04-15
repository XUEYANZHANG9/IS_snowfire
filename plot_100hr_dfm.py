
# coding: utf-8

# In[48]:

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
u = ds['fm100'].groupby('time.month').mean('time')
# average of JAS months 
v = (u.sel(month=6) + u.sel(month=7) + u.sel(month=8) + u.sel(month=9)) / 4.0

# PLOTTING 

fs = 30 ## fontsize
nbins = 11
lp = 30


model = "MIROC5"
# scenarios = ["historical", "rcp45", "rcp45", "rcp45", "rcp85", "rcp85", "rcp85"]
scenarios = ["historical", "rcp85", "rcp85", "rcp85"]
# chunks = ["1970_1999", "2010_2039", "2040_2069", "2070_2099", "2010_2039", "2040_2069", "2070_2099"]
chunks = ["1970_1999", "2010_2039", "2040_2069", "2070_2099"]
direcs = ['hist', 'rcp85_2020s', 'rcp85_2050s', 'rcp85_2080s']
titles = ['1980s', 'RCP 8.5 2020s', 'RCP 8.5. 2050s', 'RCP 8.5. 2080s']
direc = '/raid/gergel/dfm'


# ## MOUNTAIN RANGES #  

f, axes = plt.subplots(nrows=1, ncols=4, figsize=(40,6))

# mask domain
mask_domain = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/mountains', ds.lat, ds.lon)

for i, caxes in enumerate(axes):
    ax=caxes
    plt.sca(ax)
    
    direc = '/raid/gergel/dfm/%s' % direcs[i] 

    # average over models 
    # txt_files = [b for b in os.listdir(direc)]
    txt_files = ['CNRM-CM5_%s_%s.nc' %(scenarios[i], chunks[i])]      

    total = 0.0
    for ii, f in enumerate(txt_files):
	# load data
	print(os.path.join(direc, f)) 
    	ds = xray.open_dataset(os.path.join(direc,f)) 
    	u = ds['fm100'].groupby('time.month').mean('time')
    
    	# average of JAS months 
    	v = (u.sel(month=6) + u.sel(month=7) + u.sel(month=8) + u.sel(month=9)) / 4.0
		
	if ii == 0:
		ens = v
	else: 
		ens += v

	total += 1.00
    
    v = ens / total 
    v = v.where(mask_domain == 1)

    if direcs[i] == "rcp85_2080s":
        fpn = fpn_sum / total
        fpn_mountains = fpn
    
    # plot data
    if (scenarios[i] == "historical"):

	m = make_map(fs, label_parallels=True, label_meridians=True)
	x,y = m(v.lon, v.lat)

        v_hist = v
        # vmax = v_hist.max(['lat','lon'])
        vmax = 30
	vmin = v_hist.min(['lat','lon'])
       	cmap = cmap_discretize(plt.cm.viridis, 6) 
        img = m.pcolormesh(x, y, v_hist.to_masked_array(), vmin=vmin, vmax=vmax, cmap=cmap) 
	cbar = plt.colorbar(img, orientation='horizontal')
        cbar.set_ticks([np.linspace(0, vmax, 6, endpoint=True, dtype='int')])
        cbar.set_label('% DFM', rotation='horizontal', labelpad=lp)
        
    else: 

	m = make_map(fs, label_meridians=True)
	x,y = m(v.lon, v.lat) 
        v_diff = v - v_hist
	cmap = cmap_discretize(plt.cm.bwr_r, 6)

	vmin = -6 
	vmax = 6

        img = m.pcolormesh(x, y, v_diff.to_masked_array(), vmin=vmin, vmax=vmax, cmap=cmap) 
	plt.setp(ax.get_yticklabels(), visible=False)
	if chunks[i] == "2040_2069":
        	cbar = plt.colorbar(img)
        	cbar.set_ticks([np.linspace(vmin, vmax, 6, endpoint=True, dtype='int')])
        	cbar.set_label('\Delta % Diff DFM', rotation='horizontal', labelpad=lp)
    
    font = {'size' : fs}
    plt.rc('font', **font)
    
    ax.set_title(titles[i], size=fs)
    #ax.set_xticklabels(size = fs)
    
# get rid of whitespace between subplots
plt.tight_layout() 

## save plot
direc = '/raid/gergel/dfm/plots/fm100'
if not os.path.exists(direc):
    os.makedirs(direc) ## if directory doesn't exist, create it
plotname = 'fm100_mountains'
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath)


# ## LOWLAND REGIONS ##

'''

f, axes = plt.subplots(nrows=1, ncols=4, figsize=(40,6))

direc = '/raid/gergel/dfm/%s'

# mask domain
mask_domain = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/lowlands', ds.lat, ds.lon)

for i, caxes in enumerate(axes):
    ax=caxes
    plt.sca(ax)

    direc = '/raid/gergel/dfm/%s' % direcs[i]

    # average over models 
    txt_files = [b for b in os.listdir(direc)]

    total = 0.0
    for ii, f in enumerate(txt_files):
        # load data
        print(os.path.join(direc, f))
        ds = xray.open_dataset(os.path.join(direc,f))
        u = ds['fm100'].groupby('time.month').mean('time')

        # average of JAS months 
        v = (u.sel(month=7) + u.sel(month=8) + u.sel(month=9)) / 3.0

        if ii == 0:
                ens = v
        else:
                ens += v
	
	total += 1.00

    v = ens / total
    v = v.where(mask_domain == 1)

    if direcs[i] == "rcp85_2080s":
	fpn = fpn_sum / total 
	fpn_lowlands = fpn 
    
    # plot data
    if (scenarios[i] == "historical"):

	m = make_map(fs, label_parallels=True, label_meridians=True)
        x,y = m(v.lon, v.lat)

        v_hist = v
        vmax = 30
	vmin = v_hist.min(['lat','lon'])
        # img = v_hist.plot(ax=ax, vmin=vmin, vmax=vmax, add_labels=False, add_colorbar=False)
        img = m.pcolormesh(x, y, v_hist.to_masked_array(), vmin=vmin, vmax=vmax, cmap='viridis') 
	cbar = plt.colorbar(img)
        cbar.set_ticks([np.linspace(0, vmax, 6, endpoint=True, dtype='int')])
        cbar.set_label('% \n DFM', rotation='horizontal', labelpad=lp)
        
    else: 

	m = make_map(fs, label_meridians=True)
        x,y = m(v.lon, v.lat)

        v_diff = v - v_hist
        # img = v_diff.plot(ax=ax, add_labels=False, vmin=-4, vmax=4, cmap='bwr', add_colorbar=False)
        img = m.pcolormesh(x, y, v_diff.to_masked_array(), vmin=-4, vmax=4, cmap='bwr') 
	plt.setp(ax.get_yticklabels(), visible=False)
        cbar = plt.colorbar(img)
        cbar.set_ticks([np.linspace(-4, 4, 6, endpoint=True, dtype='int')])
        cbar.set_label('% \n Diff \n DFM', rotation='horizontal', labelpad=lp)
    
    font = {'size' : fs}
    plt.rc('font', **font)
    
    ax.set_title(titles[i], size=fs)
    
# get rid of whitespace between subplots
plt.tight_layout() 

## save plot
direc = '/raid/gergel/dfm/plots/fm100'
if not os.path.exists(direc):
    os.makedirs(direc) ## if directory doesn't exist, create it
plotname = 'fm100_lowlands' 
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath)
'''


