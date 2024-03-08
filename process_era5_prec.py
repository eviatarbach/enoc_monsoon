import xarray
import matplotlib.pyplot as plt
import numpy

era = xarray.open_dataset('data/era5_prec.nc')
summed = era['tp'].resample(time='D').sum().rename({'latitude': 'lat', 'longitude': 'lon'})
summed2 = summed.reindex(lat=summed.lat[::-1])
clim = summed2.loc[(summed2.time.dt.month <= 9) & (summed2.time.dt.month >= 5)]
clim_grouped = clim.assign_coords(dayofyear=clim.time.dt.strftime("%m-%d")).groupby('dayofyear')
clim_mean = clim_grouped.mean()
(clim_grouped - clim_mean).to_netcdf('data/era5_anomalies.nc')
clim_mean.to_netcdf('data/clim_mean_era5.nc')
