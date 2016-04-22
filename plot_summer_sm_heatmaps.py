
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


fs = 40 ## fontsize
nbins = 11
lp = 10
dpi = 50

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
            # diff_means.append(sm_mean - sm_hist_mean)
	    diff_means.append(perc_diff) 

    diff_means = np.around(np.asarray(diff_means),4)
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
    
    df_pivot_pvals = df_pivot_pvals.iloc[::-1].values.ravel() ## flips over the dataframe, then makes it one dimension 
                                                              ##so that it can be iterated through the same way as ax.text 
    
    return(df_pivot,diff_means,df_pivot_pvals)

'''
def denote_stat_sig(pvals,pivot_table_values,plot_obj):
    count = 0
    for text in plot_obj.texts:
        text.set_size(8)
        if pvals[count] < 0.05: 
            text.set_color('blue')
            text.set_weight('bold')
            text.set_style('italic')
        count += 1 
    return(plot_obj)
'''

lt = 30
rt = 15
fig = plt.figure(figsize=(lt,rt))

# set font properties
font = {'size' : fs}
plt.rc('font', **font)


# create colorbar axes
cax1 = plt.axes([0.1, 0.1, 0.8, 0.05])  #[left,vertical, distance from left, height] 

fig_count = 0
for scenario in scenarios: 
	for clim_period in clim_periods: 
		df_pivot, diff_means, pvals = make_df_for_heatmap(models_10, basins_10, scenario, clim_period)	
		ax = fig.add_subplot(2, 3, (fig_count + 1) ) 
		sns.heatmap(df_pivot, 
				annot=False, 
				linewidths=.5,
				cmap='RdBu',
				cbar = True if fig_count == 1 else False,
				cbar_ax=cbar_ax,  
				cbar_kws={"extend": 'min'}, 
				vmin=-50, 
				vmax=50
				cbar_kws={"extend": 'min', 
					"orientation": "horizontal", 
					"label": "% Change in Soil Moisture", 
					"size": fs})
		
		sns.heatmap(df_pivot, mask=pvals_df < 0.05, cbar=False,cmap='gray', annot=True, 
				annot_kws={"size": "10", "alpha": "0.0", "text": "%.1d"})

		if clim_period == "2020s" and scenario == "rcp45": 
			ax.set_title("2020s")
		elif clim_period == "2050s" and scenario == "rcp45": 
			ax.set_title("2050s") 
		elif clim_period == "2080s" and scenario == "rcp45":
			ax.set_title("2080s") 
		# ax = denote_stat_sig(pvals, diff_means, ax) 
		fig_count += 1 



fig.text(0.075, 0.5, 'RCP 8.5', va='center', rotation='horizontal', size = 'x-large')
fig.text(0.075, 0.93, 'RCP 4.5', va='center', rotation='horizontal', size = 'x-large')

## save plot
direc = '/raid/gergel/sm/plots'
plotname = 'heatmap_sm.png' 
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath, dpi=dpi)

