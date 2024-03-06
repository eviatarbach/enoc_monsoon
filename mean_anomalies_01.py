import xarray

obs = xarray.open_dataset('data/prec_2021.nc')
clim = obs["p"].loc[(obs.time.dt.month <= 11) & (obs.time.dt.month >= 3) & (obs.time.dt.year <= 2007) & (obs.time.dt.year >= 1950)]
clim_grouped = clim.assign_coords(dayofyear=clim.time.dt.strftime("%m-%d")).groupby('dayofyear')
clim_mean = clim_grouped.mean()
clim_mean.to_netcdf("data/clim_mean.nc")

all_dat = obs["p"].loc[(obs.time.dt.month <= 11) & (obs.time.dt.month >= 3)]
all_grouped = all_dat.assign_coords(dayofyear=all_dat.time.dt.strftime("%m-%d")).groupby('dayofyear')
anomalies = all_grouped - clim_mean
anomalies.to_netcdf('data/anomalies.nc')
