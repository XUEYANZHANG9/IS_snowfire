
# coding: utf-8

# In[46]:

import numpy as np
import xray
#from xray import ufuncs
import os
import math 
import gc 
import pandas as pd 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys 
from mpl_toolkits.axes_grid1 import make_axes_locatable

args = sys.argv[1:]
gcm = args[0]
scenario = args[1]
variable = args[2]


#gcm = 'CNRM-CM5'
#scenario = 'rcp45'


# In[48]:

direc = '/raid3/oriana/bpa/future/vic/%s/%s/fluxes/output/nc/' % (gcm,scenario)
file = 'merged.19500101-20991231.nc'
ds = xray.open_dataset(os.path.join(direc,file)) 


# In[53]:

starts = ['1969-10-1','2009-10-1','2039-10-1','2069-10-1']
ends = ['1999-10-1','2039-10-1','2069-10-1','2099-10-1']
variables = ['Runoff','SWE','Evaporation']
scenarios = ['rcp45','rcp85']
titles = ['1980s','2020s','2050s','2080s']
months = [10,11,12,1,2,3,4,5,6,7,8,9]


# In[ ]:




# In[57]:

fs = 30 ## fontsize

f, axes = plt.subplots(nrows=1, ncols=3,figsize=(10,20))
for colnum in np.arange(4):
    for rownum in np.arange(12):
        ax=axes[rownum, colnum]
        plt.sca(ax)

	## make colorbar axis 
	#divider = make_axes_locatable(plt.gca()) 
	#cax = divider.append_axes("right","5%",pad="10%") 

        vmax = ds[variable].sel(time=slice(starts[3], ends[3])).groupby(
            'time.month').mean('time').sel(month=months[rownum]).max(['lat','lon'])
        vmin = ds[variable].sel(time=slice(starts[3], ends[3])).groupby(
            'time.month').mean('time').sel(month=months[rownum]).min(['lat','lon'])
        
        ds_sel = ds[variable].sel(time=slice(starts[colnum], ends[colnum])).groupby('time.month').mean('time')
        ds_sel.sel(month=months[rownum]).plot(ax=ax,
                                             add_colorbar=False if colnum != 3 else True,
                                             add_labels=False,
                                             vmin=vmin,vmax=vmax)
        if rownum == 0:
            ax.set_title(titles[colnum],size=fs)
        if colnum == 0:
            ax.set_ylabel(str(months[rownum]),rotation=0,size=fs,labelpad=20)
        ## make labels invisible
        if rownum != 11: 
            plt.setp(axes[rownum,colnum].get_xticklabels(),visible=False)
        if colnum != 0:
            plt.setp(axes[rownum,colnum].get_yticklabels(),visible=False)
        if colnum == 3:
            cax = plt.gcf().axes[-1]
            cax.set_yticklabels(np.around(np.linspace(0,vmax,10),decimals=1),size = fs)
            cax.set_label('mm') 
## save plot
direc = '/raid9/gergel/agg_snowpack/plots_oriana/mean_monthly_spatial/%s' %variable
plotname = '%s_%s' % (gcm,scenario) 
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath)







