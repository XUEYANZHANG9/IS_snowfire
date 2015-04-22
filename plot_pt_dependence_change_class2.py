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


####################### bin by temperature and historical classifications remain constant for the future #############
## redefine rcp4.5 and 8.5 by historical indices

## historical
file = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/constantclass_ensavg_%s_hist.npz' %(basin)
data = np.load(file)
swe_rd_hist = data['swe_rd']
pr_rd_hist = data['precip_rd']
swe_tr_hist = data['swe_tr']
pr_tr_hist = data['precip_tr']
swe_sd_hist = data['swe_sd']
pr_sd_hist = data['precip_sd']

## rcp45
file = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/constantclass_ensavg_%s.npz' %(basin)
data = np.load(file)
## snow dominant
pr_sd_2010_2039_rcp45 = data['precip_rcp45_2010_2039_sd']
pr_sd_2040_2069_rcp45 = data['precip_rcp45_2040_2069_sd']
pr_sd_2070_2099_rcp45 = data['precip_rcp45_2070_2099_sd']

swe_sd_2010_2039_rcp45 = data['swe_rcp45_2010_2039_sd']
swe_sd_2040_2069_rcp45 = data['swe_rcp45_2040_2069_sd']
swe_sd_2070_2099_rcp45 = data['swe_rcp45_2070_2099_sd']

## transient
pr_tr_2010_2039_rcp45 = data['precip_rcp45_2010_2039_tr']
pr_tr_2040_2069_rcp45 = data['precip_rcp45_2040_2069_tr']
pr_tr_2070_2099_rcp45 = data['precip_rcp45_2070_2099_tr']

swe_tr_2010_2039_rcp45 = data['swe_rcp45_2010_2039_tr']
swe_tr_2040_2069_rcp45 = data['swe_rcp45_2040_2069_tr']
swe_tr_2070_2099_rcp45 = data['swe_rcp45_2070_2099_tr']

## rain dominant
pr_rd_2010_2039_rcp45 = data['precip_rcp45_2010_2039_rd']
pr_rd_2040_2069_rcp45 = data['precip_rcp45_2040_2069_rd']
pr_rd_2070_2099_rcp45 = data['precip_rcp45_2070_2099_rd']

swe_rd_2010_2039_rcp45 = data['swe_rcp45_2010_2039_rd']
swe_rd_2040_2069_rcp45 = data['swe_rcp45_2040_2069_rd']
swe_rd_2070_2099_rcp45 = data['swe_rcp45_2070_2099_rd']

## rcp85
## snow dominant
pr_sd_2010_2039_rcp85 = data['precip_rcp85_2010_2039_sd']
pr_sd_2040_2069_rcp85 = data['precip_rcp85_2040_2069_sd']
pr_sd_2070_2099_rcp85 = data['precip_rcp85_2070_2099_sd']

swe_sd_2010_2039_rcp85 = data['swe_rcp85_2010_2039_sd']
swe_sd_2040_2069_rcp85 = data['swe_rcp85_2040_2069_sd']
swe_sd_2070_2099_rcp85 = data['swe_rcp85_2070_2099_sd']


## transient
pr_tr_2010_2039_rcp85 = data['precip_rcp85_2010_2039_tr']
pr_tr_2040_2069_rcp85 = data['precip_rcp85_2040_2069_tr']
pr_tr_2070_2099_rcp85 = data['precip_rcp85_2070_2099_tr']

swe_tr_2010_2039_rcp85 = data['swe_rcp85_2010_2039_tr']
swe_tr_2040_2069_rcp85 = data['swe_rcp85_2040_2069_tr']
swe_tr_2070_2099_rcp85 = data['swe_rcp85_2070_2099_tr']


## rain dominant
pr_rd_2010_2039_rcp85 = data['precip_rcp85_2010_2039_rd']
pr_rd_2040_2069_rcp85 = data['precip_rcp85_2040_2069_rd']
pr_rd_2070_2099_rcp85 = data['precip_rcp85_2070_2099_rd']

swe_rd_2010_2039_rcp85 = data['swe_rcp85_2010_2039_rd']
swe_rd_2040_2069_rcp85 = data['swe_rcp85_2040_2069_rd']
swe_rd_2070_2099_rcp85 = data['swe_rcp85_2070_2099_rd']

#################### plot properties
lw = 1.0
fs = 10
####################

## do plots
## historical
ax5 = plt.subplot(3,1,1)
if len(swe_sd_hist) > 0:
        ax5.plot(pr_sd_hist,swe_sd_hist,'k.',linewidth=0.01,label='SD',alpha=0.1)
        slope_sd, intercept_sd, r_value_sd, p_value_sd, std_err_sd = stats.linregress(pr_sd_hist,swe_sd_hist)
        label_str = 'SD:r=%.2f, m=%.2f' %(r_value_sd,slope_sd)
        ax5.plot(pr_sd_hist,slope_sd*pr_sd_hist+intercept_sd,'k-',linewidth=1.3,label=label_str)
if len(swe_rd_hist) > 0:
        ax5.plot(pr_rd_hist,swe_rd_hist,'r.',linewidth=0.01,label='RD',alpha=0.1)
        slope_rd, intercept_rd, r_value_rd, p_value_rd, std_err_rd = stats.linregress(pr_rd_hist,swe_rd_hist)
        label_str = 'RD:r=%.2f, m=%.2f' %(r_value_rd,slope_rd)
        ax5.plot(pr_rd_hist,slope_rd*pr_rd_hist+intercept_rd,'r-',linewidth=1.3,label=label_str)
ax5.plot(pr_tr_hist,swe_tr_hist,'g.',linewidth=0.01,label='TR',alpha=0.1)
slope_tr, intercept_tr, r_value_tr, p_value_tr, std_err_tr = stats.linregress(pr_tr_hist,swe_tr_hist)
label_str = 'TR:r=%.2f, m=%.2f' %(r_value_tr,slope_tr)
ax5.plot(pr_tr_hist,slope_tr*pr_tr_hist+intercept_tr,'g-',linewidth=1.3,label=label_str)
ax5.set_title('historical',fontsize=fs)

## rcp4.5
ax2 = plt.subplot(3,1,2,sharex=ax5)
## snow dominant
if len(swe_sd_hist) > 0:
	sl, int, r, p, s_err = stats.linregress(pr_sd_2010_2039_rcp45,swe_sd_2010_2039_rcp45)
	label_str = 'SD 2010-2039:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_sd_2010_2039_rcp45),np.max(pr_sd_2010_2039_rcp45),len(pr_sd_2010_2039_rcp45))
	ax2.plot(x_plot,sl*x_plot+int,'k-',linewidth=lw,label=label_str)
	sl, int, r, p, s_err = stats.linregress(pr_sd_2040_2069_rcp45,swe_sd_2040_2069_rcp45)
	label_str = 'SD 2040-2069:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_sd_2040_2069_rcp45),np.max(pr_sd_2040_2069_rcp45),len(pr_sd_2040_2069_rcp45))
	ax2.plot(x_plot,sl*x_plot+int,'k:',linewidth=lw,label=label_str)
	sl, int, r, p, s_err = stats.linregress(pr_sd_2070_2099_rcp45,swe_sd_2070_2099_rcp45)
	label_str = 'SD 2070-2099:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_sd_2070_2099_rcp45),np.max(pr_sd_2070_2099_rcp45),len(pr_sd_2070_2099_rcp45))
	ax2.plot(x_plot,sl*x_plot+int,'k--',linewidth=lw,label=label_str)
## transient
sl, int, r, p, s_err = stats.linregress(pr_tr_2010_2039_rcp45,swe_tr_2010_2039_rcp45)
label_str = 'TR 2010-2039:r=%.2f, m=%.2f' %(r,sl)
x_plot = np.linspace(np.min(pr_tr_2010_2039_rcp45),np.max(pr_tr_2010_2039_rcp45),len(pr_tr_2010_2039_rcp45))
ax2.plot(x_plot,sl*x_plot+int,'g-',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_tr_2040_2069_rcp45,swe_tr_2040_2069_rcp45)
label_str = 'TR 2040-2069:r=%.2f, m=%.2f' %(r,sl)
x_plot = np.linspace(np.min(pr_tr_2040_2069_rcp45),np.max(pr_tr_2040_2069_rcp45),len(pr_tr_2040_2069_rcp45))
ax2.plot(x_plot,sl*x_plot+int,'g:',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_tr_2070_2099_rcp45,swe_tr_2070_2099_rcp45)
label_str = 'TR 2070-2099:r=%.2f, m=%.2f' %(r,sl)
x_plot = np.linspace(np.min(pr_tr_2070_2099_rcp45),np.max(pr_tr_2070_2099_rcp45),len(pr_tr_2070_2099_rcp45))
ax2.plot(x_plot,sl*x_plot+int,'g--',linewidth=lw,label=label_str)
## rain dominant
if len(swe_rd_hist) > 0:
	sl, int, r, p, s_err = stats.linregress(pr_rd_2010_2039_rcp45,swe_rd_2010_2039_rcp45)
	label_str = 'RD 2010-2039:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_rd_2010_2039_rcp45),np.max(pr_rd_2010_2039_rcp45),len(pr_rd_2010_2039_rcp45))
	ax2.plot(x_plot,sl*x_plot+int,'r-',linewidth=lw,label=label_str)
	sl, int, r, p, s_err = stats.linregress(pr_rd_2040_2069_rcp45,swe_rd_2040_2069_rcp45)
	label_str = 'RD 2040-2069:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_rd_2040_2069_rcp45),np.max(pr_rd_2040_2069_rcp45),len(pr_rd_2040_2069_rcp45))
	ax2.plot(x_plot,sl*x_plot+int,'r:',linewidth=lw,label=label_str)
	sl, int, r, p, s_err = stats.linregress(pr_rd_2070_2099_rcp45,swe_rd_2070_2099_rcp45)
	label_str = 'RD 2070-2099:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_rd_2070_2099_rcp45),np.max(pr_rd_2070_2099_rcp45),len(pr_rd_2070_2099_rcp45))
	ax2.plot(x_plot,sl*x_plot+int,'r--',linewidth=lw,label=label_str)

ax2.set_ylabel('SWE in mm')
ax2.set_title('RCP 4.5',fontsize=fs)

## rcp8.5
ax3 = plt.subplot(3,1,3,sharex=ax2)

## snow dominant
if len(swe_sd_hist) > 0:
	sl, int, r, p, s_err = stats.linregress(pr_sd_2010_2039_rcp85,swe_sd_2010_2039_rcp85)
	label_str = 'SD 2010-2039:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_sd_2010_2039_rcp85),np.max(pr_sd_2010_2039_rcp85),len(pr_sd_2010_2039_rcp85))
	ax3.plot(x_plot,sl*x_plot+int,'k-',linewidth=lw,label=label_str)
	sl, int, r, p, s_err = stats.linregress(pr_sd_2040_2069_rcp85,swe_sd_2040_2069_rcp85)
	label_str = 'SD 2040-2069:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_sd_2040_2069_rcp85),np.max(pr_sd_2040_2069_rcp85),len(pr_sd_2040_2069_rcp85))
	ax3.plot(x_plot,sl*x_plot+int,'k:',linewidth=lw,label=label_str)
	sl, int, r, p, s_err = stats.linregress(pr_sd_2070_2099_rcp85,swe_sd_2070_2099_rcp85)
	label_str = 'SD 2070-2099:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_sd_2070_2099_rcp85),np.max(pr_sd_2070_2099_rcp85),len(pr_sd_2070_2099_rcp85))
	ax3.plot(x_plot,sl*x_plot+int,'k--',linewidth=lw,label=label_str)
## transient
sl, int, r, p, s_err = stats.linregress(pr_tr_2010_2039_rcp85,swe_tr_2010_2039_rcp85)
label_str = 'TR 2010-2039:r=%.2f, m=%.2f' %(r,sl)
x_plot = np.linspace(np.min(pr_tr_2010_2039_rcp85),np.max(pr_tr_2010_2039_rcp85),len(pr_tr_2010_2039_rcp85))
ax3.plot(x_plot,sl*x_plot+int,'g-',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_tr_2040_2069_rcp85,swe_tr_2040_2069_rcp85)
label_str = 'TR 2040-2069:r=%.2f, m=%.2f' %(r,sl)
x_plot = np.linspace(np.min(pr_tr_2040_2069_rcp85),np.max(pr_tr_2040_2069_rcp85),len(pr_tr_2040_2069_rcp85))
ax3.plot(x_plot,sl*x_plot+int,'g:',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_tr_2070_2099_rcp85,swe_tr_2070_2099_rcp85)
label_str = 'TR 2070-2099:r=%.2f, m=%.2f' %(r,sl)
x_plot = np.linspace(np.min(pr_tr_2070_2099_rcp85),np.max(pr_tr_2070_2099_rcp85),len(pr_tr_2070_2099_rcp85))
ax3.plot(x_plot,sl*x_plot+int,'g--',linewidth=lw,label=label_str)
## rain dominant
if len(swe_rd_hist) > 0:
	sl, int, r, p, s_err = stats.linregress(pr_rd_2010_2039_rcp85,swe_rd_2010_2039_rcp85)
	label_str = 'RD 2010-2039:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_rd_2010_2039_rcp85),np.max(pr_rd_2010_2039_rcp85),len(pr_rd_2010_2039_rcp85))
	ax3.plot(x_plot,sl*x_plot+int,'r-',linewidth=lw,label=label_str)
	sl, int, r, p, s_err = stats.linregress(pr_rd_2040_2069_rcp85,swe_rd_2040_2069_rcp85)
	label_str = 'RD 2040-2069:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_rd_2040_2069_rcp85),np.max(pr_rd_2040_2069_rcp85),len(pr_rd_2040_2069_rcp85))
	ax3.plot(x_plot,sl*x_plot+int,'r:',linewidth=lw,label=label_str)
	sl, int, r, p, s_err = stats.linregress(pr_rd_2070_2099_rcp85,swe_rd_2070_2099_rcp85)
	label_str = 'RD 2070-2099:r=%.2f, m=%.2f' %(r,sl)
	x_plot = np.linspace(np.min(pr_rd_2070_2099_rcp85),np.max(pr_rd_2070_2099_rcp85),len(pr_rd_2070_2099_rcp85))
	ax3.plot(x_plot,sl*x_plot+int,'r--',linewidth=lw,label=label_str)

ax3.set_title('RCP 8.5',fontsize=fs)
ax3.set_xlabel('precip in mm')
ax3.legend(loc='lower right',prop={'size':6})
ax5.legend(loc='lower right',prop={'size':6})
ax2.legend(loc='lower right',prop={'size':6})
#ax1.legend_.remove()
plt.setp( ax5.get_xticklabels(), visible=False)
plt.setp( ax2.get_xticklabels(), visible=False)
if (basin == "northernrockies"):
        ax5.set_ylim([0, 2000])
        ax2.set_ylim([0, 2000])
        ax3.set_ylim([0, 2000])
elif (basin == "southernrockies"):
	ax5.set_ylim([0, 1400])
        ax2.set_ylim([0, 1400])
        ax3.set_ylim([0, 1400])
elif (basin == "cascades"):
        ax5.set_ylim([0, 5000])
        ax2.set_ylim([0, 5000])
        ax3.set_ylim([0, 5000])
elif (basin == "california"):
        ax5.set_ylim([0, 2500])
        ax2.set_ylim([0, 2500])
        ax3.set_ylim([0, 2500])
else:
	ax5.set_ylim([0, 350])
        ax2.set_ylim([0, 350])
        ax3.set_ylim([0, 350])



## save plot
plotname = 'RD_TR_SD_reg_constantclass_%s' %basin
direc = '/raid9/gergel/agg_snowpack/swe_t_p_reg/plots/constantclass/'
savepath = os.path.join(direc,plotname)
print ("saving figure to '%s'" %savepath)
plt.savefig(savepath)

