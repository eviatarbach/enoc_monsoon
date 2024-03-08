import numpy                                               
import xarray                                              
                                                           
n_regress_days = 29                                        
n_years_total = 107 
n_years_training = 92                                      
n_days = 275                                               
n_pcs = 2                                                  
D = 4964                                                   
                                                           
x = xarray.open_dataarray('data/prec_out.nc').values            
pcs = xarray.open_dataset('data/pcs.h5')["pcs"].values.T        
pcs = pcs.reshape(n_years_total, n_days, n_pcs)            
                                                           
n_samples = n_years_training*(n_days - 122)                
                                                           
x_new = numpy.zeros((n_samples, n_regress_days, D))        
pcs_new = numpy.zeros((n_samples, n_pcs))                  
                                                           
k = 0                                                      
for i in range(n_years_training):                          
    for j in range(61, n_days - 61):                       
        x_new[k, :, :] = x[j-n_regress_days:j, :, i]       
        pcs_new[k, :] = pcs[i, j, :]                       
        k += 1                                             
                                                           
x_new = numpy.reshape(x_new, (n_samples, -1))              
                                                           
xarray.DataArray(x_new).to_netcdf("data/x_training_past.nc")    
xarray.DataArray(pcs_new).to_netcdf("data/pcs_training_past.nc")
