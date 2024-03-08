import xarray

forecasts = xarray.open_dataset('data/seas5_forecasts.nc')

forecasts = forecasts.rename({'initial_time1_hours': 'initial_time', 'forecast_time2': 'forecast_time',
                              'g0_lat_3': 'lat', 'g0_lon_4': 'lon', 'ensemble0': 'ensemble', 'TP_GDS0_SFC': 'p'})

forecasts = forecasts.reindex(lat=forecasts.lat[::-1])

diff = forecasts['p'].isel(forecast_time=range(1, 60)).values - forecasts['p'].isel(forecast_time=range(0, 59)).values

forecasts['p'][:, :, 1:, :, :] = diff

forecasts['p'] *= 1000

model_clim = forecasts['p'].sel(initial_time=(forecasts['p'].initial_time.dt.year <= 2007) & (forecasts['p'].initial_time.dt.year >= 1993)).assign_coords(dayofyear=forecasts['p'].initial_time.dt.strftime("%m-%d")).groupby('dayofyear').mean().mean('ensemble')

model_clim.to_netcdf('data/seas5_clim.nc')

model_anomalies = forecasts['p'].assign_coords(dayofyear=forecasts['p'].initial_time.dt.strftime("%m-%d")).groupby('dayofyear') - model_clim

model_anomalies.to_netcdf('data/seas5_anomalies_combined.nc')