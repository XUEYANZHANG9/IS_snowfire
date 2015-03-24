import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import datetime
import numpy as np
import os
basins = ["cascades","california","northernrockies","southernrockies","whites"]
scenarios = ["historical","rcp45","rcp85"]
vars = ["swe","sm"]
colors = ["blue","red","black"]
colors2 = ["green","chartreuse","purple"]
for var in vars:
	for basin in basins: 
		count_swe = 0
		count_sm = 0
		plt.figure(figsize=(16,4))
		for scenario in scenarios: 
			direc = '/raid9/gergel/agg_snowpack/%s' %scenario
			file = '%s.npz' %basin
			data = np.load(os.path.join(direc,file))
			dates = data['dates']
			if (var == "swe"):
				swe = data['swe']
				plt.plot_date(dates,swe,fmt='-',color=colors[count_swe],label=scenario)
        			plt.ylabel('SWE in km^3')
        			########################### set axes
        			if (basin == 'whites'):
                			plt.ylim((0,2))
        			else:
                			plt.ylim((0,120))
        			plt.title('April 1 SWE in %s' %(basin))
				plt.legend()
        			## save plot
        			direc = '/raid9/gergel/agg_snowpack/plots/agg_swe'
        			plotname = 'swe_%s' % (basin)
        			savepath = os.path.join(direc, plotname)
        			print ("saving figure to '%s'" % savepath)
        			plt.savefig(savepath)
				count_swe += 1
			else: 
				sm_mar = data['sm_mar']
				sm_aug = data['sm_aug']
				plt.plot_date(dates,sm_mar,fmt='-',color=colors[count_sm],label='March %s' %scenario)
				plt.plot_date(dates,sm_aug,fmt='-',color=colors2[count_sm],label='August %s' %scenario)
				plt.title('Soil Moisture in %s' %basin)
				plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),ncol=1, fancybox=True, shadow=True,prop={'size':8})
				## save plot
				direc = '/raid9/gergel/agg_snowpack/plots/agg_sm'
				plotname = 'sm_%s' %basin
				savepath = os.path.join(direc,plotname)
				print("saving figure to '%s'" %savepath)
				plt.savefig(savepath)
				count_sm += 1
