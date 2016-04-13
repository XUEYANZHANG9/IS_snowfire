
# In[ ]:

## this set of functions calculates the area of a grid cell, taking elevation into account
def get_dist(lat1, long1, lat2, long2):
    ## takes in two points and returns distance between 2 locations
    import math 
    radius_of_earth = 6371.228 # in km
    ## convert from degrees to radians
    dtor = math.pi/180
    theta1= dtor*long1
    phi1 = dtor*lat1
    theta2 = dtor*long2
    phi2 = dtor*lat2
    ## use sine functions in radians (since converted above)
    term1 = math.cos(phi1)*math.cos(theta1)*math.cos(phi2)*math.cos(theta2)
    term2 = math.cos(phi1)*math.sin(theta1)*math.cos(phi2)*math.sin(theta2)
    term3 = math.sin(phi1)*math.sin(phi2)
    temp = term1+term2+term3
    distance = radius_of_earth*math.acos(temp)
    return distance

## calculating cell area function

def calc_area(lat, lon, cellsize):
    import numpy as np
    ##This function takes in longitude, latitude and grid cell size and returns the area of the grid cell 
    start_lat = lat - (cellsize/2)
    right_lon = lon + (cellsize/2)
    left_lon = lon - (cellsize/2)
    
    lat = np.absolute(lat)
    lon = np.absolute(lon)
    
    input_for_delta = lat + (cellsize/10)
    delta = get_dist(lat, lon, input_for_delta,lon)
    dist = 0
    for distance in range(0,10):
        dist = dist + get_dist(start_lat, left_lon, start_lat, right_lon)* delta
        start_lat = start_lat + (cellsize/10)
        
    cell_area = dist
    return (cell_area)


# In[ ]:

### this function takes in a basin, model and scenario as input arguments and returns latitude, longitude, SWE, and Time numpy 
### arrays

def unpack_netcdf_gen(var,mtnrange,scenario):

    from netCDF4 import Dataset
    import numpy as np
    import os
    from netCDF4 import num2date

    directory_name = '/raid9/gergel/agg_snowpack/goodleap/%s' % (mtnrange)
    file_beg = '%s_ensavg_%s_%s.nc' % (var,scenario,mtnrange)
    filename = os.path.join(directory_name,file_beg)
    print ("unpacking data from '%s'" % filename)

    ### read in latitude, longitude and variable data
    fh = Dataset(filename, mode='r') 
    lons = fh.variables['Longitude'][:]
    lats = fh.variables['Latitude'][:]
    datess = num2date(fh.variables['Time'][:],fh.variables['Time'].units)
    if (var == "SWE"):
 	varinfile = "SWE"
    elif (var == "pr"):
	varinfile = "precipitation"
    elif (var == "tasmax"):
	varinfile = "air_temp_max"
    else: 
	varinfile = "air_temp_min"
    variable = fh.variables[varinfile][:]
    fh.close()
    return (lats,lons,variable,datess)

def unpack_netcdf_file_var(direc,file,var):

        from netCDF4 import Dataset
        import numpy as np
        import os
        from netCDF4 import num2date

        filename = os.path.join(direc,file)
        # print ("unpacking data from '%s'" % filename)

        ### read in latitude, longitude and swe monthly maximum data
        fh = Dataset(filename, mode='r')
        if (var == "swe"):
                varinfile = "SWE"
	elif (var == "TotalSoilMoist"):
		varinfile = "SoilMoist"
        elif (var == "pr"):
		varinfile = "precipitation"
	elif (var == "tasmin"):
		varinfile = "air_temp_min"
	elif (var == "tasmax"):
		varinfile = "air_temp_max"
	else:
                varinfile = var
        lons = fh.variables['Longitude'][:]
        lats = fh.variables['Latitude'][:]
        var = fh.variables[varinfile][:]
        datess = num2date(fh.variables['Time'][:],fh.variables['Time'].units)
        fh.close()
        return (lats,lons,var,datess)


def unpack_netcdf(basin, model, scenario):

    from netCDF4 import Dataset 
    import numpy as np
    import os
    from netCDF4 import num2date

    directory_name = '/raid9/gergel/agg_snowpack/%s' % (basin)
    file_beg = 'SWE_%s_%s_monday1_%s_april.nc' % (scenario,model,basin)
    filename = os.path.join(directory_name,file_beg)
    print ("unpacking data from '%s'" % filename)

    ### read in latitude, longitude and swe monthly maximum data
    fh = Dataset(filename, mode='r')
    lons = fh.variables['Longitude'][:]
    lats = fh.variables['Latitude'][:]
    swe = fh.variables['SWE'][:]
    datess = num2date(fh.variables['Time'][:],fh.variables['Time'].units)
    fh.close()
    return (lats,lons,swe,datess)

def unpack_netcdf_swe_ensavg(basin,scenario):

    from netCDF4 import Dataset
    import numpy as np
    import os
    from netCDF4 import num2date

    directory_name = '/raid9/gergel/agg_snowpack/%s_%s' % (basin,basin)
    file_beg = 'SWE_ensavg_%s_%s_april.nc' % (scenario,basin)
    filename = os.path.join(directory_name,file_beg)
    print ("unpacking data from '%s'" % filename)

    ### read in latitude, longitude and swe monthly maximum data
    fh = Dataset(filename, mode='r')
    lons = fh.variables['Longitude'][:]
    lats = fh.variables['Latitude'][:]
    swe = fh.variables['SWE'][:]
    datess = num2date(fh.variables['Time'][:],fh.variables['Time'].units)
    fh.close()
    return (lats,lons,swe,datess)


def unpack_netcdf_swe_month(basin, model, scenario,month):

    from netCDF4 import Dataset
    import numpy as np
    import os
    from netCDF4 import num2date

    directory_name = '/raid9/gergel/agg_snowpack/%s_%s' % (basin,basin)
    file_beg = 'SWE_%s_%s_monday1_%s_%s.nc' % (scenario,model,basin,month)
    filename = os.path.join(directory_name,file_beg)
    print ("unpacking data from '%s'" % filename)

    ### read in latitude, longitude and swe monthly maximum data
    fh = Dataset(filename, mode='r')
    lons = fh.variables['Longitude'][:]
    lats = fh.variables['Latitude'][:]
    swe = fh.variables['SWE'][:]
    datess = num2date(fh.variables['Time'][:],fh.variables['Time'].units)
    fh.close()
    return (lats,lons,swe,datess)


# In[ ]:

### this function sums up historical SWE and only includes grid cells that have a historical mean SWE > 10 mm
### TAKES IN lats, lons, swe 
### spits out swe_aggregate (numpy array of summed up swe) 
def sum_swe(lats,lons,swe,basin,model,scenario):
    import numpy as np
    import math 
    ### start calculating area of grid cells
    resol = 0.0625
    cellsize = 0.0625
    radius_of_earth = 6371.228 # in km
    
    ## initialize array
    len_array = len(swe)
    swe_yearly_agg = np.ndarray(shape = (len_array,1), dtype=float)
    
    ## get historical SWE for model so that historical mean can be determined for mask
    scenario_for_mean = 'historical'
    lats_hist,lons_hist,swe_hist,datess_hist = unpack_netcdf(basin,model,scenario_for_mean)
    
    ## arrays for latitude and longitude values included in the historical mean mask 
    lats_lons_inc_in_mask = list()

    ################# loop through array and get latitude, longitude and swe values for each #############

    for i in np.arange(len(swe)):     ### loop over year
    
        ## initialize value of SWE for each year to zero
        swe_gridcell_total = 0
        swe_gridcell = 0
    
        for j in np.arange(len(lats)):       ### loop over latitude
            for k in np.arange(len(lons)):   ### loop over longitude
                ### don't calculate area for missing value elements
                ### isnan will convert masked values to nan's, so this statement will evaluate to false if 
                ### the value exists (and thus is not masked)
                if (math.isnan(swe[i,j,k])) == False:
                    historical_sum_swe = 0
                    for year in np.arange(len(swe_hist)):
                        historical_sum_swe += swe_hist[year,j,k]
                    mean_swe = historical_sum_swe/len(swe)
                    if (mean_swe > 10): 
                        ### calculate area of grid cell and sum up values of April 1 SWE
                        cellarea = calc_area(lats[j],lons[k],resol)
                        ## calculate amount of swe in each grid cell: swe (in mm) * area of grid cell
                        ## adjust for units: distance is in km, swe in mm
                        swe_gridcell = cellarea*(swe[i,j,k]*0.000001)
                        ## sum up swe values
                        ## swe_gridcell is the total aggregate snowpack in the masked basin on April 1 of 
                        ## the measured year 
                        swe_gridcell_total += swe_gridcell
                        points = [lats[j],lons[k]]
                        lats_lons_inc_in_mask.append(points)
                
        ## summed up yearly April 1 aggregate snowpack
        swe_yearly_agg[i] = swe_gridcell_total
    
    ##### save arrays to files for a multimodel average (and for spatial plots with lats and lons)
    ## define path based on scenario
    filearrayname = '/raid9/gergel/agg_snowpack/%s/%s_%s.npz' %(scenario,model,basin)
    np.savez(filearrayname,x=swe_yearly_agg)
    file_mask = '/raid9/gergel/agg_snowpack/%s/%s_latslonsinmask_%s.npz' %(scenario,basin,model)
    np.savez(file_mask,x=np.asarray(lats_lons_inc_in_mask))
    return (swe_yearly_agg,lats_lons_inc_in_mask)


# In[ ]:

### this function plots aggregate swe and saves the plot to a file
### TAKES IN datess,swe_yearly_agg,basin,model,scenario
def plot_swe(datess,swe_yearly_agg,basin,model,scenario):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import netCDF4
    from netCDF4 import num2date
    import os 
    plt.figure(figsize=(16,4))
    plt.plot_date(datess,swe_yearly_agg,fmt='-')
    plt.grid()
    plt.ylabel('SWE in km^3')
    ########################### set axes
    if (basin == 'whites'):
	plt.ylim((0,5))
    else:
	plt.ylim((0,120))
    plt.title('%s April 1 SWE in %s %s' %(scenario,basin,model))
    
    ## save plot 
    direc = '/raid9/gergel/agg_snowpack/plots/'
    plotname = 'April_1_SWE_%s_%s_%s' % (scenario, model, basin)
    savepath = os.path.join(direc, plotname)
    print ("saving figure to '%s'" % savepath)
    plt.savefig(savepath)


# In[ ]:

def aggregate_snowpack(basin,model,scenario):
    ####################      RUN SCRIPT       #######################
    lats,lons,swe,datess = unpack_netcdf(basin, model, scenario)
    swe_yearly_agg,lats_lons_inc_in_mask = sum_swe(lats,lons,swe,basin,model,scenario)
    plot_swe(datess,swe_yearly_agg,basin,model,scenario)
    print ("finished calculating aggregate snowpack for %s %s %s" %(basin,model,scenario))
    return (lats_lons_inc_in_mask)

def import_gridcell_elevation(soil_file):
    import numpy as np
    ## load VIC soil parameters text file
    soil_file = '/raid9/gergel/agg_snowpack/soil_avail.txt'
    soil_params = np.loadtxt(soil_file, dtype = 'string', delimiter = ',')
    ### .split() splits the line up by whitespace!! to convert to float: float(string value)
    ######################### 2nd column: latitude; 3rd column: longitude; 21st column: average elevation of grid cell
    ######## initialize np array for cell number, lat, long, elevation
    ## initialize array
    len_array = len(soil_params)
    elev_corr_info = np.ndarray(shape = (len_array,4), dtype=float) # 0th: cell num; 1st: lat; 2nd: long; 3rd: avg elevation in
                                                                    ## meters
    ## fill in array with: 1st column: grid cell number, 2nd column: latitude, 3rd column: longitude, 4th column:
    ##  elevation (in meters)
    for element in np.arange(0,len_array):
        line_loop = soil_params[element].split()
        elev_corr_info[element,0] = line_loop[1]
        elev_corr_info[element,1] = line_loop[2]
        elev_corr_info[element,2] = line_loop[3]
        elev_corr_info[element,3] = line_loop[21]
    return (elev_corr_info)

#### this function gets the corresponding latitude given a numpy array of lats, lons and elevations and inputted lat and lon points
def get_elev_for_lat_lon(elev_corr_info,lat,lon):
    """
    function takes in soil file as a numpy array and returns elevation corresponding to input lat and lon 
    """ 
    import numpy as np
    '''
    for row_num in np.arange(len(elev_corr_info)):
        if (elev_corr_info[row_num,1] == lat) and (elev_corr_info[row_num,2] == lon):
            elevation_individual_gridcell = elev_corr_info[row_num,3]
    '''
    row_ind = np.where((elev_corr_info[:,1] == lat) & (elev_corr_info[:,2] == lon))
    elev = elev_corr_info[row_ind,3][0][0]
    return(elev)

#### general version of function: takes in datess and swe arrays, removes leap years from both
def remove_leap_years(datess,swe):
    swe_wout_leap_yrs = list()
    datess_wout_leap_yrs = list()
    index_of_nonleap_yrs = list()
    for i,j in enumerate(datess):
        if (j.year%4 != 0):
            swe_wout_leap_yrs.append(swe[i])
            datess_wout_leap_yrs.append(datess[i])
            index_of_nonleap_yrs.append(i)
    return (swe_wout_leap_yrs,datess_wout_leap_yrs,index_of_nonleap_yrs)

def historical_sum_swe(lat_index,lon_index):
	'''
	this function uses the Livneh historical dataset (from 1950-2005) to check whether the historical sum of SWE 
	in the input grid cell is greater than or equal to 10 mm
	'''
	import os
	import numpy as np
	direc = '/raid9/gergel/agg_snowpack/goodleap/SWE' 
	filename = 'livneh_april1swe.nc'
	from snowpack_functions import unpack_netcdf_file_var
	lats,lons,swe,datess = unpack_netcdf_file_var(direc,filename,"swe")
	historical_sum_swe = 0
	for year in np.arange(len(swe)):
		historical_sum_swe += swe[year,lat_index,lon_index] 
	mean_swe = historical_sum_swe/len(swe)
	if mean_swe >= 10:
		return True
	else: 	
		return False 

	


def lat_lon_adjust(lat,lon,basin):
    if (basin == 'california'):
        if lat > 39.0 and lon > -120.0:
            return False
        elif lat < 38.0 and lon < -120.0:
            return False
        else:
            return True
    elif (basin == 'whites'):
        if lat > 35.0:
            return False
        elif lat < 33:
            return False
        else:
            return True

    elif (basin == 'southernrockies'):
        if lat < 36.75 and lon < -107.0:
            return False
        else:
            return True

    elif (basin == 'northernrockies'):
        if lat < 43.3 and lon < -112.0:
            return False
        elif lat > 46.0 and lon > -110.0:
            return False
        else:
            return True
    else:
        return True

## function to replace mask boxes
def mask_latlon(lat,lon,basin):
    if (basin == 'cascades'):
        ## WA
        if lat < 49.0 and lat > 45.5  and lon < -120 and lon > -122.5:
            return True
        ## OR
        elif lat < 45.5 and lat > 42 and lon < -121.35 and lon > -123.25:
            return True
        # CA
        elif lat < 42 and lat > 41.5 and lon < -120 and lon > -122.7:
            return True
        # if not in these boxes, don't include
        else:
            return False
    elif (basin == 'northernrockies'):
        # MT
        if lat < 49.0 and lat > 44.5 and lon < -109.0 and lon > -116.25:
            return True
        # ID
        elif lat < 49.0 and lat > 42.0 and lon < -111.0 and lon > -117.0:
            return True
        # WY
        elif lat < 45.0 and lat > 42.37 and lon < -107.5 and lon > -111.0:
            return True
        # if not in these boxes, don't include
	else:
            return False

    elif (basin == 'southernrockies'):
        # WY
        if lat < 42.37 and lat > 41.0 and lon < -107.0 and lon > -111.0:
            return True
        # CO
        if lat < 41.0 and lat > 37.0 and lon < -105.5 and lon > -109.0:
            return True
        # UT 1
        elif lat < 42.0 and lat > 41.0 and lon < -111.0 and lon > -112.5:
            return True
        # UT 2
        elif lat < 41.0 and lat > 40.0 and lon < -109.0 and lon > -111.0:
            return True
        # NM
        elif lat < 37.0 and lat > 35.0 and lon < -106.0 and lon > -109.0:
            return True
        # if not in these boxes, don't include
	else:
            return False

    elif (basin == 'california'):
        return True

    else:
        return True

def find_idx(v,arrmin,delta):
        ## return int((v-arrmin)/delta)
        return int(round((v-arrmin)/delta))
'''
def make_map():
	from mpl_toolkits.basemap import Basemap 
        m=Basemap(llcrnrlon=-125,llcrnrlat=31,urcrnrlon = -102.5,urcrnrlat=50,projection='cyl',lat_1=33,lat_2=42,lon_0=-110,
                resolution='c')
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
        m.drawlsmask(land_color='grey',ocean_color='lightblue',lakes=True)
        return(m)
'''

def make_map(fs, label_parallels=None, label_meridians=None):
    """
    function that creates map using Basemap. 
    
    Requires fontsize, and optional arguments governing labels for parallels and meridians. 
    
    Returns matplotlib plotting object. 
    """
    
    from mpl_toolkits.basemap import Basemap
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
    m.drawlsmask(land_color='silver',ocean_color='lightskyblue',lakes=True,resolution='c')
    return(m)

def mesh_gridify(lats,lons,data):
        from snowpack_functions import find_idx
        import numpy as np
        min_lat = np.min(lats)
        min_lon = np.min(lons)
        max_lat = np.max(lats)
        max_lon = np.max(lons)
        latt = np.arange(min_lat,max_lat+0.125,0.0625)
        lng = np.arange(min_lon,max_lon+0.125,0.0625)
        gridz = np.nan*np.empty((len(latt),len(lng)))
        count = 0
        for hlat,hlng in zip(lats,lons):
                gridz[find_idx(hlat,latt[0],0.0625),find_idx(hlng,lng[0],0.0625)] = data[count][0]
                count += 1
        masked_gridz = np.ma.masked_where(np.isnan(gridz),gridz)
        lons_mesh,lats_mesh = np.meshgrid(lng,latt)
        return(lons_mesh,lats_mesh,masked_gridz)

def mask_out_other_mtns(lat,lon):
	if lon < -122 and lat < 40.7: 
        	return False 
    	elif lon < -123:
        	return False
    	elif lon > -119.75 and lon < -114 and lat > 39 and lat < 43.1:
        	return False
    	elif lat > 30 and lat < 39 and lon > -117.6 and lon < -114:
		return False 
	elif lat > 31.5 and lat < 37 and lon > -114 and lon < -111:
        	return False
    	## oregon
    	elif lat < 46 and lat > 43 and lon > -121 and lon < -117:
        	return False
    	## utah
    	elif lat > 37 and lat < 39 and lon > -114 and lon < -109: 
        	return False
    	elif lat > 39 and lat < 42 and lon > -114 and lat < -112:
        	return False
    	elif lat < 35 and lon < -117:
        	return False
    	elif lat > 43 and lat < 44 and lon > -117 and lon < -116: 
        	return False
    	elif lat > 42 and lat < 49 and lon > -108 and lon < -103:
        	return False
    	elif lat < 33: 
        	return False
    	elif lat < 35.5 and lon > -108.75:
        	return False
    	elif lat > 45 and lon > -109:
        	return False
    	elif lat > 48 and lon > -110:
        	return False
    	elif lat > 35 and lat < 37 and lon < -108 and lon > -111: 
        	return False
    	elif lon > -114 and lon < -113 and lat > 37 and lat < 43: 
        	return False
    	elif lat > 45 and lat < 47 and lon > -118.25 and lon < -117:
        	return False
    	elif lat > 38.5 and lon > -104.5:
        	return False
    	else:
        	return True

def mask_out_mtns_vf(arr,lat,lon):
        if lon < -122 and lat < 40.7:
                return np.nan
        elif lon < -123:
                return np.nan
        elif lon > -119.75 and lon < -114 and lat > 39 and lat < 43.1:
                return np.nan
        elif lat > 30 and lat < 39 and lon > -117.6 and lon < -114:
                return np.nan
        elif lat > 31.5 and lat < 37 and lon > -114 and lon < -111:
                return np.nan
        ## oregon
        elif lat < 46 and lat > 43 and lon > -121 and lon < -117:
                return np.nan
        ## utah
        elif lat > 37 and lat < 39 and lon > -114 and lon < -109:
                return np.nan
        elif lat > 39 and lat < 42 and lon > -114 and lat < -112:
                return np.nan
        elif lat < 35 and lon < -117:
                return np.nan
        elif lat > 43 and lat < 44 and lon > -117 and lon < -116:
                return np.nan
        elif lat > 42 and lat < 49 and lon > -108 and lon < -103:
                return np.nan
        elif lat < 33:
                return np.nan
        elif lat < 35.5 and lon > -108.75:
                return np.nan
        elif lat > 45 and lon > -109:
                return np.nan
        elif lat > 48 and lon > -110:
                return np.nan
        elif lat > 35 and lat < 37 and lon < -108 and lon > -111:
                return np.nan
        elif lon > -114 and lon < -113 and lat > 37 and lat < 43:
                return np.nan
        elif lat > 45 and lat < 47 and lon > -118.25 and lon < -117:
                return np.nan
        elif lat > 38.5 and lon > -104.5:
                return np.nan
        else:
		return arr
 
