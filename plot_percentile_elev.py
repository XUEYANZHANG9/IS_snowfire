### plot elevation percentiles
# basins=['cascades','california','southernrockies','northernrockies','whites']
import numpy as np
import sys
from snowpack_functions import unpack_netcdf_swe_ensavg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import netCDF4
from netCDF4 import num2date
import os
fig=plt.figure()
'''
args = sys.argv[0]
basin = args[0]
'''
basin='whites'
scenarios = ["historical","rcp45","rcp85"]
for s in np.arange(3):
        lats, lons, swe, datess = unpack_netcdf_swe_ensavg(basin,scenarios[s])
        filename = '/raid9/gergel/agg_snowpack/%s/percentiles_elev_ensavg_SWE_%s.npz' %(scenarios[s],basin)
	data = np.load(filename) 
        ax=fig.add_subplot(3,1,s+1)
        e_10 = data['e_10']
        e_25 = data['e_25']
        e_50 = data['e_50']
        e_75 = data['e_75']
        e_90 = data['e90']
        ax.plot_date(datess[9:],e_10,fmt='r-',label='10th')
        ax.plot_date(datess[9:],e_25,fmt='b-',label='25th')
        ax.plot_date(datess[9:],e_50,fmt='k-',label='50th')
        ax.plot_date(datess[9:],e_75,fmt='g-',label='75th')
        ax.plot_date(datess[9:],e_90,fmt='m-',label='90th')
	if (basin == 'california'):
		ax.set_ylim([1400,3600])
	elif (basin == 'northernrockies'):
		ax.set_ylim([1100,3000])
	elif (basin == 'southernrockies'): 
		ax.set_ylim([2000,3700])
	else:
		ax.set_ylim([800,2000])
ax.set_ylabel('elev (m)')
ax.legend(loc='center left', prop={'size':6},bbox_to_anchor=(1,0.5),ncol=1,fancybox=True,shadow=True)
# plt.ylabel('elev (m)')
plt.suptitle('10-year EnsAvg Elevations for %s' %(basin))
## save plot
direc = '/raid9/gergel/agg_snowpack/plots/'
plotname = 'percentiles_elev_ensavg_SWE_%s' % (basin)
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath)

