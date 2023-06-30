import numpy as np
import pandas as pd
import os
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import netCDF4
import math

folder_path = '../satellitegrids/' # Where grids are
grids = []
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    grids.append(file_path)
#grids.remove('../satellitegrids/.DS_Store') # If using notebook


# Check if grids have more than 4 variables
# grids_not4 = []
# for grid in range(len(grids)):
#     dataset = Dataset(grids[grid])
#     variable_names = dataset.variables.keys()
#     if len(variable_names) > 4:
#         grids_not4.append(grids[grid])

# FOR MULTIPLE .nc FILES
for grid in range(len(grids)):
    elements = grids[grid].split("_")
    
    dataset = Dataset(grids[grid])
    variable_names = dataset.variables.keys()
    names_list = list(variable_names)
    lons = dataset.variables['lon'][:]
    lats = dataset.variables['lat'][:]
    first = dataset.variables[names_list[0]][:] # masked
    unmasked_first = first.filled(fill_value=np.nan)

    # Adjust next two lines for to change output of .nc file
    name_of_satellite = (elements[0] + '_' + elements[1]).replace('../satellitegrids/', '') 
    grp = netCDF4.Dataset('outputnc/' + str(name_of_satellite)+ f'_lvl3_{elements[3]}_{elements[4]}_{names_list[0]}' + '.dos.5m.nc', 'w', format='NETCDF4')
  
    # dimensions
    grp.createDimension('lat',len(lats))
    grp.createDimension('lon',len(lons))
    lat = grp.createVariable('lat',np.double,('lat',))
    lon = grp.createVariable('lon',np.double,('lon',))
    z = grp.createVariable('z',np.float32,('lat','lon')) # make sure this is UPSIDE DOWN WHEN YOU WRITE TO FILE!!!
    lat.units = 'degrees'
    lon.units = 'degrees'
    lat.long_name = 'latitude'
    lon.long_name = 'longitude'

    lat[:] = lats
    lon[:] = lons
    z[:,:] = unmasked_first
    grp.close()
