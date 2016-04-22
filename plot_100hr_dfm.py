
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
lp = 10
dpi = 150 

model = "MIROC5"
# scenarios = ["historical", "rcp45", "rcp45", "rcp45", "rcp85", "rcp85", "rcp85"]
scenarios = ["historical", "rcp85", "rcp85", "rcp85", "historical", "rcp85", "rcp85", "rcp85"]
chunks = ["1970_1999", "2010_2039", "2040_2069", "2070_2099", "1970_1999", "2010_2039", "2040_2069", "2070_2099"]
# chunks = ["1970_1999", "2010_2039", "2040_2069", "2070_2099"]
direcs = ['hist', 'rcp85_2020s', 'rcp85_2050s', 'rcp85_2080s', 'hist', 'rcp85_2020s', 'rcp85_2050s', 'rcp85_2080s']
titles = ['1980s', 'RCP 8.5 2020s', 'RCP 8.5 2050s', 'RCP 8.5 2080s']
direc = '/raid/gergel/dfm'


# ## MOUNTAIN RANGES #  

f, axes = plt.subplots(nrows=2, ncols=4, figsize=(30,15)) 

# mask domain
mask_domain_mtns = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/mountains', ds.lat, ds.lon)
mask_domain_lowlands = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/lowlands', ds.lat, ds.lon)

for i, caxes in enumerate(axes.ravel()):
    ax=caxes
    plt.sca(ax)
    
    if i < 4:
	mask_domain = mask_domain_mtns
    else: 
	mask_domain = mask_domain_lowlands 

    direc = '/raid/gergel/dfm/%s' % direcs[i] 

    # average over models 
    txt_files = [b for b in os.listdir(direc)]
    # txt_files = ['CNRM-CM5_%s_%s.nc' %(scenarios[i], chunks[i])]      

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
 
    # plot data
    if (scenarios[i] == "historical"):

	if i == 0: 
		m = make_map(fs, label_parallels=True)
	else: 
		m = make_map(fs, label_parallels=True, label_meridians=True)
	x,y = m(v.lon, v.lat)

        v_hist = v
        # vmax = v_hist.max(['lat','lon'])
        vmin = 0
	vmax = 28
       	cmap = cmap_discretize(plt.cm.viridis_r, 7) 
        img_h = m.pcolormesh(x, y, v_hist.to_masked_array(), vmin=vmin, vmax=vmax, cmap=cmap)        

    else: 

	if i < 4: 
		m = make_map(fs) 
	else: 
		m = make_map(fs, label_meridians=True)

	x,y = m(v.lon, v.lat) 
        # v_diff = v - v_hist
	v_diff = ( (v - v_hist) / ( (v + v_hist) / 2.0 ) ) * 100.0 

	cmap = cmap_discretize(plt.cm.bwr_r, 10)

	'''
	vmin = -6 
	vmax = 6
	'''
	vmin = -25
	vmax = 25  

        img_f = m.pcolormesh(x, y, v_diff.to_masked_array(), vmin=vmin, vmax=vmax, cmap=cmap) 
	plt.setp(ax.get_yticklabels(), visible=False)
	
    font = {'size' : fs}
    plt.rc('font', **font)

    if i < 4:
	title_above = '%s \n ' % titles[i]  
    	ax.set_title(title_above, size=fs)
    
# get rid of whitespace between subplots
plt.subplots_adjust(wspace=0.1, hspace=None, left=0.05, right=0.98, top=0.9, bottom=0.2) 

# add delineation between rows
#plt.text(0.075, 0.5, 'Mountain Ranges', va='center', rotation='horizontal',size = 'x-large')
#plt.text(0.075, 0.93, 'Lowland Regions', va='center', rotation='horizontal',size = 'x-large')

# create colorbars 
cax1 = plt.axes([0.04, 0.1, 0.22, 0.05]) #[left,vertical, distance from left, height]
cbar = plt.colorbar(img_h, cax=cax1, orientation='horizontal')
cbar.set_ticks([np.linspace(0, 28, 8, endpoint=True, dtype='int')])
cbar.set_label('% DFM', rotation='horizontal', labelpad=lp)

cax2 = plt.axes([0.47, 0.1, 0.35, 0.05]) #[left,vertical, distance from left, height]
cbar = plt.colorbar(img_f, cax=cax2, orientation='horizontal')
cbar.set_ticks([np.linspace(vmin, vmax, 11, endpoint=True, dtype='int')])
# cbar.set_label('$\Delta$ % Difference DFM', rotation='horizontal', labelpad=lp) 
cbar.set_label('% Difference in DFM', rotation='horizontal', labelpad=lp) 

## save plot
direc = '/raid/gergel/dfm/plots/fm100'
if not os.path.exists(direc):
    os.makedirs(direc) ## if directory doesn't exist, create it
plotname = 'fm100'
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath, dpi=dpi)


