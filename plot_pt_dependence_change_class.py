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

## get data
## historical
file = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/ensavg_%s_%s.npz' %(basin,"historical")
data = np.load(file)
temp_avg_hist = data['temp_avg']
precip_hist = data['precip']
swe_hist = data['swe']
## rcp4.5
file = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/ensavg_%s_%s.npz' %(basin,"rcp45")
data = np.load(file)
swe_2010_2039_rcp45 = data['swe_2010_2039']
swe_2040_2069_rcp45 = data['swe_2040_2069']
swe_2070_2099_rcp45 = data['swe_2070_2099']
precip_2010_2039_rcp45 = data['precip_2010_2039']
precip_2040_2069_rcp45 = data['precip_2040_2069']
precip_2070_2099_rcp45 = data['precip_2070_2099']
temp_avg_2010_2039_rcp45 = data['temp_avg_2010_2039']
temp_avg_2040_2069_rcp45 = data['temp_avg_2040_2069']
temp_avg_2070_2099_rcp45 = data['temp_avg_2070_2099']
## rcp8.5
file = '/raid9/gergel/agg_snowpack/swe_t_p_reg/proc_data/ensavg_%s_%s.npz' %(basin,"rcp85")
data = np.load(file)
swe_2010_2039_rcp85 = data['swe_2010_2039']
swe_2040_2069_rcp85 = data['swe_2040_2069']
swe_2070_2099_rcp85 = data['swe_2070_2099']
precip_2010_2039_rcp85 = data['precip_2010_2039']
precip_2040_2069_rcp85 = data['precip_2040_2069']
precip_2070_2099_rcp85 = data['precip_2070_2099']
temp_avg_2010_2039_rcp85 = data['temp_avg_2010_2039']
temp_avg_2040_2069_rcp85 = data['temp_avg_2040_2069']
temp_avg_2070_2099_rcp85 = data['temp_avg_2070_2099']



####################### bin by temperature and change classification in the future ############################
## hist class 
## snow dominant
rd_cut = 278.15
sd_cut = 267.15
pr_sd_hist = precip_hist[temp_avg_hist <= sd_cut]
swe_sd_hist = swe_hist[temp_avg_hist <= sd_cut]
## transient
pr_tr_hist = precip_hist[(temp_avg_hist > sd_cut) & (temp_avg_hist < rd_cut)]
swe_tr_hist = swe_hist[(temp_avg_hist > sd_cut) & (temp_avg_hist < rd_cut)]
## rain dominant
pr_rd_hist = precip_hist[temp_avg_hist >= rd_cut]
swe_rd_hist = swe_hist[temp_avg_hist >= rd_cut]

## rcp45
## snow dominant
pr_sd_2010_2039_rcp45 = precip_2010_2039_rcp45[temp_avg_2010_2039_rcp45 <= sd_cut]
pr_sd_2040_2069_rcp45 = precip_2040_2069_rcp45[temp_avg_2040_2069_rcp45 <= sd_cut]
pr_sd_2070_2099_rcp45 = precip_2070_2099_rcp45[temp_avg_2070_2099_rcp45 <= sd_cut]

swe_sd_2010_2039_rcp45 = swe_2010_2039_rcp45[temp_avg_2010_2039_rcp45 <= sd_cut]
swe_sd_2040_2069_rcp45 = swe_2040_2069_rcp45[temp_avg_2040_2069_rcp45 <= sd_cut]
swe_sd_2070_2099_rcp45 = swe_2070_2099_rcp45[temp_avg_2070_2099_rcp45 <= sd_cut]

## transient
pr_tr_2010_2039_rcp45 = precip_2010_2039_rcp45[(temp_avg_2010_2039_rcp45 > sd_cut) & (temp_avg_2010_2039_rcp45 < rd_cut)]
pr_tr_2040_2069_rcp45 = precip_2040_2069_rcp45[(temp_avg_2040_2069_rcp45 > sd_cut) & (temp_avg_2040_2069_rcp45 < rd_cut)]
pr_tr_2070_2099_rcp45 = precip_2070_2099_rcp45[(temp_avg_2070_2099_rcp45 > sd_cut) & (temp_avg_2070_2099_rcp45 < rd_cut)]

swe_tr_2010_2039_rcp45 = swe_2010_2039_rcp45[(temp_avg_2010_2039_rcp45 > sd_cut) & (temp_avg_2010_2039_rcp45 < rd_cut)]
swe_tr_2040_2069_rcp45 = swe_2040_2069_rcp45[(temp_avg_2040_2069_rcp45 > sd_cut) & (temp_avg_2040_2069_rcp45 < rd_cut)]
swe_tr_2070_2099_rcp45 = swe_2070_2099_rcp45[(temp_avg_2070_2099_rcp45 > sd_cut) & (temp_avg_2070_2099_rcp45 < rd_cut)]


## rain dominant
pr_rd_2010_2039_rcp45 = precip_2010_2039_rcp45[temp_avg_2010_2039_rcp45 >= rd_cut]
pr_rd_2040_2069_rcp45 = precip_2040_2069_rcp45[temp_avg_2040_2069_rcp45 >= rd_cut]
pr_rd_2070_2099_rcp45 = precip_2070_2099_rcp45[temp_avg_2070_2099_rcp45 >= rd_cut]

swe_rd_2010_2039_rcp45 = swe_2010_2039_rcp45[temp_avg_2010_2039_rcp45 >= rd_cut]
swe_rd_2040_2069_rcp45 = swe_2040_2069_rcp45[temp_avg_2040_2069_rcp45 >= rd_cut]
swe_rd_2070_2099_rcp45 = swe_2070_2099_rcp45[temp_avg_2070_2099_rcp45 >= rd_cut]


## rcp85
## snow dominant
pr_sd_2010_2039_rcp85 = precip_2010_2039_rcp85[temp_avg_2010_2039_rcp85 <= sd_cut]
pr_sd_2040_2069_rcp85 = precip_2040_2069_rcp85[temp_avg_2040_2069_rcp85 <= sd_cut]
pr_sd_2070_2099_rcp85 = precip_2070_2099_rcp85[temp_avg_2070_2099_rcp85 <= sd_cut]

swe_sd_2010_2039_rcp85 = swe_2010_2039_rcp85[temp_avg_2010_2039_rcp85 <= sd_cut]
swe_sd_2040_2069_rcp85 = swe_2040_2069_rcp85[temp_avg_2040_2069_rcp85 <= sd_cut]
swe_sd_2070_2099_rcp85 = swe_2070_2099_rcp85[temp_avg_2070_2099_rcp85 <= sd_cut]

## transient
pr_tr_2010_2039_rcp85 = precip_2010_2039_rcp85[(temp_avg_2010_2039_rcp85 > sd_cut) & (temp_avg_2010_2039_rcp85 < rd_cut)]
pr_tr_2040_2069_rcp85 = precip_2040_2069_rcp85[(temp_avg_2040_2069_rcp85 > sd_cut) & (temp_avg_2040_2069_rcp85 < rd_cut)]
pr_tr_2070_2099_rcp85 = precip_2070_2099_rcp85[(temp_avg_2070_2099_rcp85 > sd_cut) & (temp_avg_2070_2099_rcp85 < rd_cut)]

swe_tr_2010_2039_rcp85 = swe_2010_2039_rcp85[(temp_avg_2010_2039_rcp85 > sd_cut) & (temp_avg_2010_2039_rcp85 < rd_cut)]
swe_tr_2040_2069_rcp85 = swe_2040_2069_rcp85[(temp_avg_2040_2069_rcp85 > sd_cut) & (temp_avg_2040_2069_rcp85 < rd_cut)]
swe_tr_2070_2099_rcp85 = swe_2070_2099_rcp85[(temp_avg_2070_2099_rcp85 > sd_cut) & (temp_avg_2070_2099_rcp85 < rd_cut)]

## rain dominant
pr_rd_2010_2039_rcp85 = precip_2010_2039_rcp85[temp_avg_2010_2039_rcp85 >= rd_cut]
pr_rd_2040_2069_rcp85 = precip_2040_2069_rcp85[temp_avg_2040_2069_rcp85 >= rd_cut]
pr_rd_2070_2099_rcp85 = precip_2070_2099_rcp85[temp_avg_2070_2099_rcp85 >= rd_cut]

swe_rd_2010_2039_rcp85 = swe_2010_2039_rcp85[temp_avg_2010_2039_rcp85 >= rd_cut]
swe_rd_2040_2069_rcp85 = swe_2040_2069_rcp85[temp_avg_2040_2069_rcp85 >= rd_cut]
swe_rd_2070_2099_rcp85 = swe_2070_2099_rcp85[temp_avg_2070_2099_rcp85 >= rd_cut]


## cdf function
def calc_cdf(data):
	sorted_data = np.sort(data)
	yvals = np.arange(len(sorted_data))/float(len(sorted_data))
	return (sorted_data,yvals)

## plots: for historical, scatter plots and cdfs have separate y axes
### historical

####################### set plot properties
fs = 10
#######################
ax1 = plt.subplot(3,1,1)
if len(swe_sd_hist) > 0:
	x_cdf_sd_hist,y_cdf_sd_hist = calc_cdf(swe_sd_hist)
        ax1.plot(x_cdf_sd_hist,y_cdf_sd_hist,'k-',linewidth=1.0,label='SD CDF')
ax2 = ax1.twinx()
if len(swe_sd_hist) > 0:
	ax2.plot(swe_sd_hist,pr_sd_hist,'k.',linewidth=0.01,label='SD',alpha=0.05)
if len(swe_rd_hist) > 0:
	ax2.plot(swe_rd_hist,pr_rd_hist,'r.',linewidth=0.01,label='RD',alpha=0.05)
	x_cdf_rd_hist,y_cdf_rd_hist = calc_cdf(swe_rd_hist)
	ax1.plot(x_cdf_rd_hist,y_cdf_rd_hist,'r-',linewidth=1.0,label='RD CDF')
ax2.plot(swe_tr_hist,pr_tr_hist,'g.',linewidth=0.01,label='TR',alpha=0.05)
## plot cdf's of each
x_cdf_tr_hist,y_cdf_tr_hist = calc_cdf(swe_tr_hist)
ax1.plot(x_cdf_tr_hist,y_cdf_tr_hist,'g-',linewidth=1.0,label='TR CDF')
ax2.set_ylabel('precip in mm') 
ax1.set_title('historical',fontsize=fs) 

### rcp4.5
ax3 = plt.subplot(3,1,2,sharex=ax2)
x_cdf,y_cdf = calc_cdf(swe_sd_2010_2039_rcp45)
ax3.plot(x_cdf,y_cdf,'k-',linewidth=1.0,label='2010-2039')
x_cdf,y_cdf = calc_cdf(swe_sd_2040_2069_rcp45)
ax3.plot(x_cdf,y_cdf,'k:',linewidth=1.0,label='2040-2069')
x_cdf,y_cdf = calc_cdf(swe_sd_2070_2099_rcp45)
ax3.plot(x_cdf,y_cdf,'k--',linewidth=1.0,label='2070-2099')

x_cdf,y_cdf = calc_cdf(swe_rd_2010_2039_rcp45)
ax3.plot(x_cdf,y_cdf,'r-',linewidth=1.0,label='2010-2039')
x_cdf,y_cdf = calc_cdf(swe_rd_2040_2069_rcp45)
ax3.plot(x_cdf,y_cdf,'r:',linewidth=1.0,label='2040-2069')
x_cdf,y_cdf = calc_cdf(swe_rd_2070_2099_rcp45)
ax3.plot(x_cdf,y_cdf,'r--',linewidth=1.0,label='2070-2099')


x_cdf,y_cdf = calc_cdf(swe_tr_2010_2039_rcp45)
ax3.plot(x_cdf,y_cdf,'g-',linewidth=1.0,label='2010-2039')
x_cdf,y_cdf = calc_cdf(swe_tr_2040_2069_rcp45)
ax3.plot(x_cdf,y_cdf,'g:',linewidth=1.0,label='2040-2069')
x_cdf,y_cdf = calc_cdf(swe_tr_2070_2099_rcp45)
ax3.plot(x_cdf,y_cdf,'g--',linewidth=1.0,label='2070-2099')

# ax3.set_ylabel('SWE in mm') 
ax3.set_title('RCP4.5',fontsize=fs)
# ax3.legend(loc='lower right')

## rcp8.5
ax4 = plt.subplot(3,1,3,sharex=ax2)
x_cdf,y_cdf = calc_cdf(swe_sd_2010_2039_rcp85)
ax4.plot(x_cdf,y_cdf,'k-',linewidth=1.0,label='2010-2039')
x_cdf,y_cdf = calc_cdf(swe_sd_2040_2069_rcp85)
ax4.plot(x_cdf,y_cdf,'k:',linewidth=1.0,label='2040-2069')
x_cdf,y_cdf = calc_cdf(swe_sd_2070_2099_rcp85)
ax4.plot(x_cdf,y_cdf,'k--',linewidth=1.0,label='2070-2099')

x_cdf,y_cdf = calc_cdf(swe_rd_2010_2039_rcp85)
ax4.plot(x_cdf,y_cdf,'r-',linewidth=1.0,label='2010-2039')
x_cdf,y_cdf = calc_cdf(swe_rd_2040_2069_rcp85)
ax4.plot(x_cdf,y_cdf,'r:',linewidth=1.0,label='2040-2069')
x_cdf,y_cdf = calc_cdf(swe_rd_2070_2099_rcp85)
ax4.plot(x_cdf,y_cdf,'r--',linewidth=1.0,label='2070-2099')


x_cdf,y_cdf = calc_cdf(swe_tr_2010_2039_rcp85)
ax4.plot(x_cdf,y_cdf,'g-',linewidth=1.0,label='2010-2039')
x_cdf,y_cdf = calc_cdf(swe_tr_2040_2069_rcp85)
ax4.plot(x_cdf,y_cdf,'g:',linewidth=1.0,label='2040-2069')
x_cdf,y_cdf = calc_cdf(swe_tr_2070_2099_rcp85)
ax4.plot(x_cdf,y_cdf,'g--',linewidth=1.0,label='2070-2099')

ax4.set_xlabel('swe in mm')
ax3.set_ylabel('probability')
ax4.legend(loc='lower right',prop={'size':8})
ax1.legend(loc='lower right',prop={'size':8})
ax2.legend(loc='upper right',prop={'size':8})
ax4.set_title('RCP8.5',fontsize=fs)
plt.setp( ax2.get_xticklabels(), visible=False)
plt.setp( ax3.get_xticklabels(), visible=False)
plt.setp( ax1.get_xticklabels(), visible=False)

## save plot
plotname = 'RD_TR_SD_reg_changeclass_%s' %basin
direc = '/raid9/gergel/agg_snowpack/swe_t_p_reg/plots/changeclass/'
savepath = os.path.join(direc,plotname)
print ("saving figure to '%s'" %savepath)
plt.savefig(savepath)

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
ax5.set_ylabel('SWE in mm')
ax5.set_title('historical')

## rcp4.5
ax2 = plt.subplot(3,1,2,sharex=ax5)
lw = 0.3
## snow dominant 
sl, int, r, p, s_err = stats.linregress(pr_sd_2010_2039_rcp45,swe_sd_2010_2039_rcp45)
label_str = 'SD 2010-2039:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_sd_2010_2039_rcp45,sl*pr_sd_2010_2039_rcp45+int,'k-',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_sd_2040_2069_rcp45,swe_sd_2040_2069_rcp45)
label_str = 'SD 2040-2069:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_sd_2040_2069_rcp45,sl*pr_sd_2040_2069_rcp45+int,'k:',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_sd_2070_2099_rcp45,swe_sd_2070_2099_rcp45)
label_str = 'SD 2070-2099:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_sd_2070_2099_rcp45,sl*pr_sd_2070_2099_rcp45+int,'k--',linewidth=lw,label=label_str)
## transient 
sl, int, r, p, s_err = stats.linregress(pr_tr_2010_2039_rcp45,swe_tr_2010_2039_rcp45)
label_str = 'TR 2010-2039:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_tr_2010_2039_rcp45,sl*pr_tr_2010_2039_rcp45+int,'g-',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_tr_2040_2069_rcp45,swe_tr_2040_2069_rcp45)
label_str = 'TR 2040-2069:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_tr_2040_2069_rcp45,sl*pr_tr_2040_2069_rcp45+int,'g:',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_tr_2070_2099_rcp45,swe_tr_2070_2099_rcp45)
label_str = 'TR 2070-2099:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_tr_2070_2099_rcp45,sl*pr_tr_2070_2099_rcp45+int,'g--',linewidth=lw,label=label_str)
## rain dominant 
sl, int, r, p, s_err = stats.linregress(pr_rd_2010_2039_rcp45,swe_rd_2010_2039_rcp45)
label_str = 'RD 2010-2039:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_rd_2010_2039_rcp45,sl*pr_rd_2010_2039_rcp45+int,'r-',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_rd_2040_2069_rcp45,swe_rd_2040_2069_rcp45)
label_str = 'RD 2040-2069:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_rd_2040_2069_rcp45,sl*pr_rd_2040_2069_rcp45+int,'r:',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_rd_2070_2099_rcp45,swe_rd_2070_2099_rcp45)
label_str = 'RD 2070-2099:r=%.2f, m=%.2f' %(r,sl)
ax2.plot(pr_rd_2070_2099_rcp45,sl*pr_rd_2070_2099_rcp45+int,'r--',linewidth=lw,label=label_str)

ax2.set_ylabel('SWE in mm')
ax2.set_title('rcp 4.5')

## rcp8.5 
ax3 = plt.subplot(3,1,3,sharex=ax2)

## snow dominant
sl, int, r, p, s_err = stats.linregress(pr_sd_2010_2039_rcp85,swe_sd_2010_2039_rcp85)
label_str = 'SD 2010-2039:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_sd_2010_2039_rcp85,sl*pr_sd_2010_2039_rcp85+int,'k-',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_sd_2040_2069_rcp85,swe_sd_2040_2069_rcp85)
label_str = 'SD 2040-2069:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_sd_2040_2069_rcp85,sl*pr_sd_2040_2069_rcp85+int,'k:',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_sd_2070_2099_rcp85,swe_sd_2070_2099_rcp85)
label_str = 'SD 2070-2099:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_sd_2070_2099_rcp85,sl*pr_sd_2070_2099_rcp85+int,'k--',linewidth=lw,label=label_str)
## transient
sl, int, r, p, s_err = stats.linregress(pr_tr_2010_2039_rcp85,swe_tr_2010_2039_rcp85)
label_str = 'TR 2010-2039:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_tr_2010_2039_rcp85,sl*pr_tr_2010_2039_rcp85+int,'g-',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_tr_2040_2069_rcp85,swe_tr_2040_2069_rcp85)
label_str = 'TR 2040-2069:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_tr_2040_2069_rcp85,sl*pr_tr_2040_2069_rcp85+int,'g:',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_tr_2070_2099_rcp85,swe_tr_2070_2099_rcp85)
label_str = 'TR 2070-2099:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_tr_2070_2099_rcp85,sl*pr_tr_2070_2099_rcp85+int,'g--',linewidth=lw,label=label_str)
## rain dominant
sl, int, r, p, s_err = stats.linregress(pr_rd_2010_2039_rcp85,swe_rd_2010_2039_rcp85)
label_str = 'RD 2010-2039:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_rd_2010_2039_rcp85,sl*pr_rd_2010_2039_rcp85+int,'r-',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_rd_2040_2069_rcp85,swe_rd_2040_2069_rcp85)
label_str = 'RD 2040-2069:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_rd_2040_2069_rcp85,sl*pr_rd_2040_2069_rcp85+int,'r:',linewidth=lw,label=label_str)
sl, int, r, p, s_err = stats.linregress(pr_rd_2070_2099_rcp85,swe_rd_2070_2099_rcp85)
label_str = 'RD 2070-2099:r=%.2f, m=%.2f' %(r,sl)
ax3.plot(pr_rd_2070_2099_rcp85,sl*pr_rd_2070_2099_rcp85+int,'r--',linewidth=lw,label=label_str)

ax3.set_ylabel('SWE in mm')
ax3.set_title('rcp8.5')
ax3.set_xlabel('precip in mm')
ax3.set_title('RCP8.5')
ax3.legend(loc='lower right',prop={'size':6})
ax5.legend(loc='lower right',prop={'size':6})
ax5.get_legend()
ax2.legend(loc='lower right',prop={'size':6})
#ax1.legend_.remove()
plt.setp( ax5.get_xticklabels(), visible=False)
plt.setp( ax2.get_xticklabels(), visible=False)
if (basin == "northernrockies"):
	ax5.set_ylim([0, 2000])
	ax2.set_ylim([0, 2000])
	ax3.set_ylim([0, 2000])

## save plot
plotname = 'RD_TR_SD_reg_constantclass_%s' %basin
direc = '/raid9/gergel/agg_snowpack/swe_t_p_reg/plots/constantclass/'
savepath = os.path.join(direc,plotname)
print ("saving figure to '%s'" %savepath)
plt.savefig(savepath)
 
