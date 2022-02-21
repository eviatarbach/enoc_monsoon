import numpy
import xarray

n_regress_days = 29
half_regress_days = 14
n_years_total = 43
n_years_training = 43
n_days = 275
n_pcs = 2
D = 1190
year0 = 1950

anomalies = xarray.open_dataarray('era5_anomalies.nc')
x = anomalies.sel(time=anomalies.time.dt.year <= 1992).stack(stacked=['lat', 'lon']).values
x = x.reshape(n_years_total, n_days, D)
pcs = xarray.open_dataset('pcs.h5')["pcs"].values.T
pcs = pcs.reshape(115, n_days, n_pcs)

n_samples = n_years_training*(n_days - 122)

x_new = numpy.zeros((n_samples, n_regress_days, D))
pcs_new = numpy.zeros((n_samples, n_pcs))

k = 0
for year in range(year0, year0 + n_years_training):
    for j in range(61, n_days - 61):
        x_new[k, :, :] = x[year-year0, j:j+n_regress_days, :]
        pcs_new[k, :] = pcs[year-year0+49, j, :]
        k += 1

x_new = numpy.reshape(x_new, (n_samples, -1))

xarray.DataArray(x_new).to_netcdf("x_training_future_era.nc")
xarray.DataArray(pcs_new).to_netcdf("pcs_training_future_era.nc")
