
# coding: utf-8

# In[ ]:

def estimate_relative_humidity(q,t_avg,lat,lon):
    ## estimates relative humidity using hypsometric equation for pressure, virtual temperature and 
    ## average temperature 
    import numpy as np
    from snowpack_functions import get_elev_for_lat_lon,import_gridcell_elevation 
    #################### CONSTANTS ###############################
    Rd = 287.04 ## J kg^-1 K ^-1
    p1 = 100000 ## Pa
    T0 = 273.15 ## reference temperature
    g = 9.81 ## m / s^2
    
    ## need to get elevations for grid cells
    soil_file = '/raid9/gergel/agg_snowpack/soil_avail.txt'
    elev_corr_info = import_gridcell_elevation(soil_file) 
    h = get_elev_for_lat_lon(elev_corr_info,lat,lon)
    
    ##  Tv = T(1 + 0.61w)
    Tv = t_avg * (1 + 0.61*q)
    ## p = e ^ (-(((z_2 - z_1) * g)/ (Rd*Tv) - ln(p1)))
    hg = h * g
    RdTv = Rd * Tv

    p = np.exp(-((np.divide(hg,RdTv.air_temp_min)) - math.log(p1)))
    ## RH = 0.263*p*q[exp(17.67*T - T0)/(T - 29.65)]^-1
    
    RH = 0.263*p*q * ((np.exp((17.67 * (t_avg - T0))/ (t_avg - 29.65)))**-1)
    
    return (RH)

def estimate_emc(RH,t):
    if RH < 10: 
        EMC = 0.03229 + 0.281073*RH - 0.000578*t_avg*RH
    elif RH >= 10 and RH <= 50:
        EMC = 2.22749 - 0.160107*RH - 0.014784*t_avg
    else: 
        EMC = 21.0606 + (0.005565*(RH**2)) - (0.00035*RH*t_avg) - (0.483199*RH)
    return(EMC)

def nfdrs_climate_class(lon):
    ## use eastern boundary of the Cascades to delineate (this might need refinement)
    if lon > -120.5:
        climate_class = 2
        wetrat = 0.25
    else:
        climate_class = 3
        wetrat = 0.05
    return(climate_class,wetrat)

def make_map(fs, label_parallels=None, label_meridians=None):
    """
    function that creates map using Basemap. 
    
    Requires fontsize, and optional arguments governing labels for parallels and meridians. 
    
    Returns matplotlib plotting object. 
    """

    from mpl_toolkits.basemap import Basemap
    import numpy as np
    ## 
    m=Basemap(llcrnrlon=-125,llcrnrlat=31,urcrnrlon = -102.5,urcrnrlat=50,projection='cyl',lat_1=33,lat_2=42,lon_0=-110,
            resolution='i',fix_aspect=True)
    # m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    m.drawmapboundary()

    m.drawparallels(np.arange(-90.,120.,10.)) # draw parallels
    m.drawmeridians(np.arange(0.,420.,10.)) # draw meridians

    if label_parallels:
        m.drawparallels(np.arange(-90.,120.,10.),labels=[1,0,0,0],size=fs) # draw parallels
    if label_meridians:
        m.drawmeridians(np.arange(0.,420.,10.),labels=[0,0,0,1],size=fs) # draw meridians
    m.drawlsmask(land_color='silver',ocean_color='lightblue',lakes=True,resolution='c')
    return(m)

def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.
    cmap: colormap instance, eg. cm.jet. 
    N: number of colors.
      
    Example
    x = resize(arange(100), (5,100))
    djet = cmap_discretize(cm.jet, 5)
    imshow(x, cmap=djet)
    """
    if type(cmap) == str:
        cmap = get_cmap(cmap)
    colors_i = concatenate((linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) for i in xrange(N+1) ]
    # Return colormap object.
    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)
