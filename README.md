# Code for "Improved subseasonal prediction of South Asian monsoon rainfall using data-driven forecasts of oscillatory modes"

This repository contains the code for the paper "Improved subseasonal prediction of South Asian monsoon rainfall using data-driven forecasts of oscillatory modes" by Eviatar Bach, V. Krishnamurthy, Safa Mote, Jagadish Shukla, A. Surjalal Sharma, Eugenia Kalnay, and Michael Ghil.

All the code was written by Eviatar Bach. You can contact me with any questions at eviatarbach@protonmail.com.

The code requires download of the following data:
- India Meteorological Department daily gridded precipitation data since 1901. This data can be downloaded [here](https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html). Note, however, that the data used in the manuscript was an older version of the dataset, and may subtly differ from the linked one; the NetCDF structure may also be different.
- ERA5 reanalysis precipitation data since 1950 at 1 degree resolution. This data can be downloaded [here](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form). A template download script is provided in `retrieve_prec.py`; note, however, that you will likely have to download the data in parts and combine it due to limitations on download size.
- SEAS5 ECMWF precipitation forecasts. This data can be downloaded [here](https://cds.climate.copernicus.eu/cdsapp#!/dataset/seasonal-original-single-levels?tab=form). A template script is provided in `retrieve_seas5.py`; as for ERA5, however, note that the data may have to be downloaded in parts.

The following steps can then be followed to carry out the analyses in the paper. Alternatively, the raw and processed forecasts are provided as `data/all_res_uncorr` `data/all_res_corr` (see the `enoc_rev.ipynb` notebook for how to open and use this data).

Instead of training the neural networks in steps 8 and 9, the pre-trained network weights are also provided.

Steps for processing data and carrying out analysis:
1. Save the IMD data as `data/prec.nc`. Download hourly ERA5 rainfall since 1950 at 1 degree resolution, save as `data/era5_prec.nc`. Download the SEAS5 ECMWF forecasts and save as `data/seas5_forecasts.nc`.
4. Run `conda env create -f environment.yml`, `conda activate enoc_monsoon`, and `python -m ipykernel install --user --name enoc_monsoon --display-name="EnOC monsoon"`.
5. Run `python mean_anomalies_01.py` to take the mean and anomalies of the IMD rainfall data, between March and November.
6. Run `python collapse_02.py` to extract the data corresponding to the monsoon region.
7. Run `julia --project ssa_prec_03.jl` to run multichannel singular spectrum analysis (M-SSA) on the rainfall.
8. Run `julia --project miso_eof_04.jl` to take the leading empirical orthogonal functions (EOFs) of the leading monsoon intraseasonal oscillation mode.
9. Run `python process_era5_prec.py` to take the mean and anomalies of the ERA5 rainfall data.
10. Run `python prepare_nn_era_centered.py`, `python prepare_nn_era_future.py`, and `python prepare_nn_past.py` to prepare the data for neural network training.
11. Run `python regress_nn_centered_era.py`, `python regress_nn_future_era.py` to train the neural networks.
12. Run the Jupyter notebook `enoc_rev.ipynb` with the `enoc_monsoon` kernel to apply the Ensemble Oscillation Correction (EnOC) method to correct forecasts and generate figures.
