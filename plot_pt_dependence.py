#!/bin/python

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

## get command line arguments
args = sys.argv[1:]
basin = args[0]
scenario = args[1]

## get data
filename = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/ensavg_%s_%s.npz' %(basin,scenario)
data = np.load(filename)
temp_max = data['temp_max']
temp_min = data['temp_min']
precip = data['precip']
swe = data['swe']
temp_avg = data['temp_avg']
temp_max = temp_max[~np.isnan(temp_max)]
temp_min = temp_min[~np.isnan(temp_min)]
temp_avg = temp_avg[~np.isnan(temp_avg)]
precip = precip[~np.isnan(precip)]
swe = swe[~np.isnan(temp_max)]

## do regression analysis 
sl_tmax,int_tmax,r_tmax,p_tmax,std_tmax = stats.linregress(temp_max,swe)
sl_tmin,int_tmin,r_tmin,p_tmin,std_tmin = stats.linregress(temp_min,swe)
sl_tavg,int_tavg,r_tavg,p_tavg,std_tavg = stats.linregress(temp_avg,swe)
sl_pr,int_pr,r_pr,p_pr,std_pr = stats.linregress(precip,swe)

## make plots
plt.figure(figsize=(16,4))
plt.ylabel('SWE in mm')
plt.xlabel('temp in deg C')
plt.plot(temp_avg,swe,'m*')
## plot regression lines
plt.plot(temp_max,sl_tmax*temp_max+int_tmax,'r',label='Tmax')
plt.plot(temp_min,sl_tmin*temp_min+int_tmin,'b',label='Tmin')
plt.plot(temp_avg,sl_tavg*temp_avg+int_tavg,'g',label='Tavg')

plotname = 'temp_reg_%s_%s' % (basin,scenario)
direc = '/raid9/gergel/agg_snowpack/swe_t_p_reg/plots/'
savepath = os.path.join(direc,plotname)
print ("saving figure to '%s'" %savepath)
plt.savefig(savepath)

plt.figure(figsize=(16,4))
plt.plot(precip,swe,'b*')
plt.ylabel('SWE in mm')
plt.xlabel('precip in mm')
plt.plot(precip,sl_pr*precip+int_pr,'k',label='precip')

plt.legend(loc='center left',prop={'size':6})

plotname = 'pr_reg_%s_%s' % (basin,scenario)
direc = '/raid9/gergel/agg_snowpack/swe_t_p_reg/plots/'
savepath = os.path.join(direc,plotname)
print ("saving figure to '%s'" %savepath)
plt.savefig(savepath)

####################### bin by temperature #############################
pr_sd = precip[temp_avg <= 271]
swe_sd = swe[temp_avg <= 271]
if len(swe_sd) > 0:
	sl_sd,int_sd,r_sd,p_sd,std_sd = stats.linregress(pr_sd,swe_sd)
pr_tr = precip[(temp_avg > 271) & (temp_avg < 275)]
swe_tr = swe[(temp_avg > 271) & (temp_avg < 275)]
sl_tr,int_tr,r_tr,p_tr,std_tr = stats.linregress(pr_tr,swe_tr)
pr_rd = precip[temp_avg >= 275]
swe_rd = swe[temp_avg >= 275]
if len(swe_rd) > 0:
	sl_rd,int_rd,r_rd,p_rd,std_rd = stats.linregress(pr_rd,swe_rd)
	
plt.figure(figsize=(16,4))
if len(swe_sd) > 0:
	plt.plot(pr_sd,sl_sd*pr_sd+int_sd,'k',label='SD',linewidth=3.0)
	plt.plot(pr_sd,swe_sd,'k.',linewidth=0.2)
if len(swe_rd) > 0:
	plt.plot(pr_rd,sl_rd*pr_rd+int_rd,'r',label='RD',linewidth=3.0)
	plt.plot(pr_rd,swe_rd,'r.',linewidth=0.2)
plt.plot(pr_tr,sl_tr*pr_tr+int_tr,'g',label='TR',linewidth=3.0)
plt.plot(pr_tr,swe_tr,'g.',linewidth=0.2)
plt.ylabel('SWE in mm')
plt.xlabel('precip in mm')
plt.legend(loc='upper left',prop={'size':10})
if len(swe_rd) == 0:
	plt.title('TR: r = %f, SD: r = %f' %(r_tr,r_sd))
else: 
	plt.title('RD: r = %f, TR: r = %f, SD: r = %f' %(r_rd,r_tr,r_sd))
if (basin == "california"):
	plt.xlim([0,3000])
	plt.ylim([0,2500])
elif (basin == "cascades"):
	plt.xlim([0,6000])
	plt.ylim([0,5000])
elif (basin == "northernrockies"):
	plt.xlim([0,2500])
	plt.ylim([0,2500])
elif (basin == "southernrockies"):
	plt.xlim([0,1400])
	plt.ylim([0,1600])
else:
	plt.xlim([0,700])
	plt.ylim([0,350])

plotname = 'RD_TR_SD_reg_%s_%s' % (basin,scenario)
direc = '/raid9/gergel/agg_snowpack/swe_t_p_reg/plots/'
savepath = os.path.join(direc,plotname)
print ("saving figure to '%s'" %savepath)
plt.savefig(savepath)

 
