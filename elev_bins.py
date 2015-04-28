
# In[*]:

import sys
import os
import numpy as np
import matplotlib
# get_ipython().magic(u'matplotlib inline')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from snowpack_functions import get_elev_for_lat_lon,import_gridcell_elevation
basins = ["cascades","california","northernrockies","whites","southernrockies"]
# basin = "california"
scenarios = ["historical","rcp45","rcp45","rcp45","rcp85","rcp85","rcp85"] 
datanames = ['swe','swe_2010_2039','swe_2040_2069','swe_2070_2099','swe_2010_2039','swe_2040_2069','swe_2070_2099'] 


# In[*]:

lw = 2.0
offset = 60
fig = plt.figure(figsize=(20,14))
for ba in np.arange(len(basins)):
    basin = basins[ba] 
    for scenario,dataname in zip(scenarios,datanames): 
        file = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/ensavg_%s_%s.npz' %(basin,scenario)
        data = np.load(file)
        swe = data[dataname]
        lats = data['lats']
        lons = data['lons']
        ## get elevation information
        soil_file = '/raid9/gergel/agg_snowpack/soil_avail.txt'
        elev_corr_info  = import_gridcell_elevation(soil_file)
        ## example of calling function: elev_individual_gridcell = get_elev_for_lat_lon(elev_corr_info,actual_lat,actual_lon)
        swe_500 = list()
        swe_1000 = list()
        swe_1500 = list()
        swe_2000 = list()
        swe_2500 = list()
        swe_3000 = list()
        swe_3500 = list() 
        swe_4000 = list()
        count = 0
        for lat,lon in zip(lats,lons): 
            elev = get_elev_for_lat_lon(elev_corr_info,lat,lon) 
            if elev > 0 and elev <= 750:
                swe_500.append(swe[count]) 
            elif elev > 750 and elev <= 1250:
                swe_1000.append(swe[count])
            elif elev > 1250 and elev <= 1750:
                swe_1500.append(swe[count])
            elif elev > 1750 and elev <= 2250:
                swe_2000.append(swe[count])
            elif elev > 2250 and elev <= 2750:
                swe_2500.append(swe[count])
            elif elev > 2750 and elev <= 3250:
                swe_3000.append(swe[count]) 
            elif elev > 3250 and elev <= 3750:
                swe_3500.append(swe[count])
            else: 
                swe_4000.append(swe[count]) 
            count += 1 
        ############################################## DO PLOT #############################################################
        ax = fig.add_subplot(1,5,ba+1)
        swees = [swe_500,swe_1000,swe_1500,swe_2000,swe_2500,swe_3000,swe_3500,swe_4000]
        elevations = [500,1000,1500,2000,2500,3000,3500,4000]
        # colors = ['r','b','g','k','b','g','k']
        countswe = 0
        for swelist in swees: 
            swe_array = np.asarray(swelist)
            if len(swelist) > 0:
                meanswe = np.mean(swe_array)
                minswe = np.min(swe_array)
                maxswe = np.max(swe_array)
                swe10 = np.percentile(swe_array,10)
                swe90 = np.percentile(swe_array,90) 
                ## y value
                if (scenario == "historical"): 
                    elevmet = elevations[countswe]
                    cr = 'r'
                elif (scenario == "rcp45") and (dataname == 'swe_2010_2039'):
                    elevmet = elevations[countswe] + offset
                    cr = 'g'
                elif (scenario == "rcp45") and (dataname == 'swe_2040_2069'):
                    elevmet = elevations[countswe] + offset*2
                    cr = 'b'
                elif (scenario == "rcp45") and (dataname == 'swe_2070_2099'):
                    elevmet = elevations[countswe] + offset*3
                    cr = 'k'
                elif (scenario == "rcp85") and (dataname == 'swe_2010_2039'):
                    elevmet = elevations[countswe] - offset
                    cr = 'g'
                elif (scenario == "rcp85") and (dataname == 'swe_2040_2069'):
                    elevmet = elevations[countswe] - offset*2
                    cr = 'b'
                else: 
                    elevmet = elevations[countswe] - offset*3 
                    cr = 'k'
                ## minimum range
                xmin = np.arange(minswe,swe10,1)
                ax.plot(xmin,np.ones(len(xmin))*elevmet,color=cr,linestyle='--',linewidth=lw)
                ## maximum range
                xmax = np.arange(swe90,maxswe,1)
                ax.plot(xmax,np.ones(len(xmax))*elevmet,color=cr,linestyle='--',linewidth=lw) 
                ## 10-90 range
                xmid = np.arange(swe10,swe90,1)
                ax.plot(xmid,np.ones(len(xmid))*elevmet,color=cr,linestyle='-',linewidth=lw) 
                ## mean
                ax.plot(meanswe,elevmet,'o',color=cr) 
                ## 10th
                ax.plot(swe10,elevmet,'s',color=cr)
                ## 90th
                ax.plot(swe90,elevmet,'s',color=cr)
            ax.set_ylim((500,4000)) 
            countswe += 1 


# In[*]:

plotname = 'elevs_swe'
direc='/raid9/gergel/agg_snowpack/'
savepath = os.path.join(direc,plotname)
plt.savefig(savepath)
print("plot successfully saved") 

    


# In[*]:




# In[*]:



