import xarray
import numpy

n_years = 116
n_days = 275  # May, June, July, August, September
D = 4964

prec = xarray.open_dataset('data/anomalies.nc')

m = prec["p"]["time"].dt.month
mask = (m >= 3) & (m <= 11)
prec_masked = prec["p"][mask]
mask_latlon = ~numpy.isnan(prec["p"][mask][0, :, :])

#years = set(prec_masked.time.dt.year.values)
years = range(1901, 1901+n_years)

prec_full = numpy.zeros((n_days, D, n_years))

for i, year in enumerate(years):
    prec_full[:, :, i] = prec_masked[prec_masked.time.dt.year == year].values[:, mask_latlon]

xarray.DataArray(prec_full, name="prec").to_netcdf('data/prec_out.nc')
