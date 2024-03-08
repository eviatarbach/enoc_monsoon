import cdsapi
 
c = cdsapi.Client()
r = c.retrieve(
    'reanalysis-era5-single-levels-preliminary-back-extension', {
            'variable'    : 'total_precipitation',
            'product_type': 'reanalysis',
            'year'        : [str(y) for y in range(1950, 2022)],
            'month'       : ['03', '04', '05', '06', '07', '08', '09', '10', '11'],
            'time'        : [
                '00:00','01:00','02:00',
                '03:00','04:00','05:00',
                '06:00','07:00','08:00',
                '09:00','10:00','11:00',
                '12:00','13:00','14:00',
                '15:00','16:00','17:00',
                '18:00','19:00','20:00',
                '21:00','22:00','23:00'
            ],
            'day': [str(d).zfill(2) for d in range(1, 32)],
            'format'      : 'netcdf',
            'area': [39, 66, 6, 100],
            'grid'    : '1.0/1.0',
    })
r.download('data/era5_prec.nc')
