
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import os
import datetime
import numpy as np
from snowpack_functions import unpack_netcdf_file_var
import seaborn as sns 
import pandas as pd 
import xarray as xray 
from dfm_functions import make_mask 


fs = 9 ## fontsize
nbins = 11
lp = 5
dpi = 400

scenarios = ["rcp45", "rcp85"]
clim_periods = ["2020s", "2050s", "2080s"] 
variables=["soilmoisture"]

models = ['CNRM-CM5','NorESM1-M','IPSL-CM5A-MR','CanESM2','CCSM4','HadGEM2-CC365','HadGEM2-ES365','MIROC5','bcc-csm1-1-m',
          'CSIRO-Mk3-6-0'] 

basins = ["cascades","california","northernrockies","southernrockies","whites","missouri","nwinterior","coastalnorth",
          "coastalsouth","lowercolorado","greatbasin"]


basins_corr_formatting = ["Cascades","Sierra Nevada","Northern Rockies","Southern Rockies","White Mountains","Missouri",
          "Northwest Interior","Coastal North","Coastal South","Lower Colorado","Great Basin"]
basins_10 = np.asarray(basins_corr_formatting*10)
models_10 = np.asarray(models*11).reshape(11,10).T.ravel()


# df = pd.DataFrame(data=d,index=np.arange(110))

# df_pivot = df.pivot("Regions", "GCMs", "means")

# SOIL MOISTURE HEATMAP IN 30 YEAR CHUNKS WITH STATISTICAL SIGNIFICANCE: CHANGE IN MEANS NORMALIZED (Figure 10)

def make_df_for_heatmap(modelss,basinss,scenario,clim_period):
    from scipy import stats
    diff_means = list()
    pvals = list()
    for model in models: 
        for basin in basins: 

            direc = '/raid9/gergel/agg_snowpack/goodleap/'

	    # historical
            filename = 'tmp_%s_TotalSoilMoist_%s.nc' % (model, "historical")
            ds = xray.open_dataset(os.path.join(direc, filename))

	    # mask domain 
            mask_direc = '/raid9/gergel/agg_snowpack/gridcells_is_paper/%s' % basin
            mask_domain = make_mask(mask_direc, ds.Latitude, ds.Longitude) 
            ds = ds.where(mask_domain == 1) 

	    ds_hist = ds['SoilMoist'].sel(Time=slice('1969-10-1', '1999-9-30'))	    
	    ds_hist_gb_mean = ds_hist.groupby('Time.month').mean('Time')
	    ds_summer_mean_hist = (ds_hist_gb_mean.sel(month=6) + ds_hist_gb_mean.sel(month=7) + ds_hist_gb_mean.sel(month=8)) / 3.0

	    sm_hist = ds_summer_mean_hist.mean(['Latitude', 'Longitude']) 
	    sm_hist_mean = ds_summer_mean_hist.mean() 

	    # future 
	    filename = 'tmp_%s_TotalSoilMoist_%s.nc' % (model, scenario)
            ds = xray.open_dataset(os.path.join(direc, filename))

            # mask domain
	    ds = ds.where(mask_domain == 1) 

	    if clim_period == "2020s": 
		 ds_fut = ds['SoilMoist'].sel(Time=slice('2009-10-1', '2039-9-30'))
	    elif clim_period == "2050s":
		 ds_fut = ds['SoilMoist'].sel(Time=slice('2039-10-1', '2069-9-30'))
	    else: 
		 ds_fut = ds['SoilMoist'].sel(Time=slice('2069-10-1', '2099-9-30'))

            ds_fut_gb = ds_fut.groupby('Time.month').mean('Time')
	    ds_summer_mean = (ds_fut_gb.sel(month=6) + ds_fut_gb.sel(month=7) + ds_fut_gb.sel(month=8)) / 3.0

	    sm = ds_summer_mean.mean(['Latitude', 'Longitude']) 
            sm_mean = ds_summer_mean.mean()

	    # try percent difference instead of difference in mean 
	    perc_diff = ( (sm_mean - sm_hist_mean) / ( (sm_mean + sm_hist_mean) / 2.0 ) ) * 100.0             
            
            pvals.append(stats.ttest_ind(sm_hist,sm,equal_var=False)[1])
    
            diff_means.append(float(sm_mean - sm_hist_mean))
	    # diff_means.append(perc_diff) 

    #diff_means = np.around(np.asarray(diff_means),4)
    diff_means = np.asarray(diff_means)
    pvals = np.asarray(pvals)

    d = {'GCMs': modelss, 'Regions': basinss, 'means': diff_means}
    d_pvals = {'GCMs': modelss, 'Regions': basinss, 'means': pvals}
    df = pd.DataFrame(data=d,index=np.arange(110))
    df_pvals = pd.DataFrame(data=d_pvals,index=np.arange(110))
    df_pivot = df.pivot("Regions", "GCMs", "means")
    df_pivot_pvals = df_pvals.pivot("Regions", "GCMs", "means")
    
    df_pivot = df_pivot.reindex_axis(["Cascades","Sierra Nevada","Northern Rockies","Southern Rockies","White Mountains","Missouri",
                                  "Northwest Interior","Coastal North","Coastal South","Lower Colorado","Great Basin"], 
                                     axis=0)
    
    df_pivot_pvals = df_pivot_pvals.reindex_axis(["Cascades","Sierra Nevada","Northern Rockies","Southern Rockies","White Mountains","Missouri",
                                  "Northwest Interior","Coastal North","Coastal South","Lower Colorado","Great Basin"], 
                                                 axis=0)
    
    df_pivot_pvals_rav = df_pivot_pvals.iloc[::-1].values.ravel() ## flips over the dataframe, then makes it one dimension 
                                                              ##so that it can be iterated through the same way as ax.text 
    
    # df_pivot = df_pivot[df_pivot.values].astype(float) # or int

    return(df_pivot, df_pivot_pvals)

lp = 15 
lt = 6.6
rt = 6
fig = plt.figure(figsize=(lt,rt))

rc={'font.size': fs, 'axes.labelsize': fs, 'xtick.major.size': fs, 'xtick.minor.size': fs, 'legend.fontsize': fs, 
    'axes.titlesize': fs, 'xtick.labelsize': fs, 'ytick.labelsize': fs, 'axes.labelpad': lp}

sns.set(rc=rc) 
sns.set_context(rc=rc)

# set font properties
# font = {'size' : fs}
# plt.rc('font', **font)


# create colorbar axes
cbar_ax = plt.axes([0.15, 0.05, 0.8, 0.05])  #[left,vertical, distance from left, height] 
# cbar_ax.tick_params(labelsize=25, size=25)


vmin = -75
vmax = 75

fig_count = 0

nums = [1, 2, 3, 4, 5, 6] 

for scenario in scenarios: 
	for clim_period in clim_periods: 
		df_pivot, pvals_df = make_df_for_heatmap(models_10, basins_10, scenario, clim_period)	
		print(type(df_pivot)) 
		print(fig_count + 1) 
		ax = fig.add_subplot(2, 3, nums[fig_count]) 
		print(df_pivot) 
		img = sns.heatmap(df_pivot, 
				annot=False, 
				cbar=False if fig_count > 0 else True, 
				cbar_ax=cbar_ax, 
				linewidths=.5, 
				square=True,  
				cmap='RdBu', 
				vmin=vmin, vmax=vmax, 
				cbar_kws={"orientation": "horizontal", "label": "% Change in Soil Moisture"}
				)
		
		# sns.heatmap(df_pivot, mask=pvals_df < 0.05, cbar=False,cmap='gray', annot=False)

		if clim_period == "2020s" and scenario == "rcp45": 
			ax.set_title("2020s")
		elif clim_period == "2050s" and scenario == "rcp45": 
			ax.set_title("2050s") 
		elif clim_period == "2080s" and scenario == "rcp45":
			ax.set_title("2080s") 

		# ax = denote_stat_sig(pvals, diff_means, ax) 
		'''
		if fig_count == 4: 
			ax.set_xlabel('GCMs', size=fs) 
		if fig_count == 0 or fig_count == 3: 
			ax.set_ylabel('Regions', size=fs) 
		'''		
		
		if fig_count < 3: 
			ax.xaxis.set_visible(False)
		if fig_count != 0 and fig_count != 3: 
			ax.yaxis.set_visible(False) 

		fig_count += 1 

'''
cbar = ax.colorbar(cax=cbar_ax, orientation='horizontal', extend='both')
cbar.set_ticks([np.linspace(vmin, vmax, 10, endpoint=True, dtype='int')])
cbar.set_label('%% Change in Soil Moisture', rotation='horizontal', labelpad=lp)
'''

# img.set(xlabel='GCMs', ylabel='Regions')

# get rid of whitespace between subplots
plt.subplots_adjust(wspace=0.05, hspace=0.1, left=0.15, right=0.98, top=0.9, bottom=0.4)

fig.text(0.075, 0.65, 'RCP 8.5', va='center', rotation='horizontal', size = fs)
fig.text(0.075, 0.93, 'RCP 4.5', va='center', rotation='horizontal', size = fs)

## save plot
direc = '/raid/gergel/sm/plots'
plotname = 'heatmap_sm.tiff' 
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath, bbox_inches='tight', format='tiff', dpi=dpi)

