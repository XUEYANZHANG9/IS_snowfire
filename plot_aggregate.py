def plot_swe(dates,swe,sm_march,sm_august,basin,scenario):
	import matplotlib
    	matplotlib.use('Agg')
    	import matplotlib.pyplot as plt
    	import netCDF4
    	from netCDF4 import num2date
    	import os
	import datetime 
	if (scenario == "historical"):
		base = datetime.datetime(1950, 4, 1)
		end_date = datetime.datetime(2006, 4, 1)
	else: 
		base = datetime.datetime(2006, 4, 1)
                end_date = datetime.datetime(2100, 4, 1)
	#dates = arr = [base + datetime.timedelta(years=i) for i in range(0, (end_date-base).years)] 
	###################### SWE plot #######################
    	plt.figure(figsize=(16,4))
    	plt.plot_date(dates,swe,fmt='-')
    	plt.ylabel('SWE in km^3')
    	########################### set axes
    	if (basin == 'whites'):
        	plt.ylim((0,5))
    	else:
        	plt.ylim((0,120))
    	plt.title('%s April 1 SWE in %s' %(scenario,basin))
	## save plot
    	direc = '/raid9/gergel/agg_snowpack/plots/agg_swe'
    	plotname = 'swe_%s_%s' % (scenario, basin)
    	savepath = os.path.join(direc, plotname)
    	print ("saving figure to '%s'" % savepath)
    	plt.savefig(savepath)
	###################### SM plot ########################	
	plt.figure(figsize=(16,4))
	plt.plot_date(dates,sm_mar,'r-',label='March')
	plt.plot_date(dates,sm_aug,'b-',label='August')
	plt.legend()
	plt.title('%s Soil Moisture in %s' %(scenario,basin))
	direc = '/raid9/gergel/agg_snowpack/plots/agg_sm'
        plotname = 'sm_%s_%s' % (scenario, basin)
        savepath = os.path.join(direc, plotname)
        print ("saving figure to '%s'" % savepath)
        plt.savefig(savepath)


import numpy as np
import os
basins = ["cascades","california","northernrockies","southernrockies","whites"]
scenarios = ["historical","rcp45","rcp85"]
for basin in basins: 
	for scenario in scenarios: 
		direc = '/raid9/gergel/agg_snowpack/%s' %scenario
		file = '%s.npz' %basin
		data = np.load(os.path.join(direc,file))
		swe = data['swe']
		sm_mar = data['sm_mar']
		sm_aug = data['sm_aug']
		dates = data['dates']
		plot_swe(dates,swe,sm_mar,sm_aug,basin,scenario)
