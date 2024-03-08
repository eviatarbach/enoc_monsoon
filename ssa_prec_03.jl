using Serialization
using Statistics

using NetCDF
using HDF5

include("ssa.jl")
using .SSA

M = 61
n_years = 107

x = ncread("data/prec_out.nc", "prec")
x = permutedims(x, [3, 2, 1])
x = Array{Float32, 3}(x)

x_ssa = x[:, :, 1:n_years]

ssa_info = SSA.ssa_decompose(x_ssa, M)

r = SSA.ssa_reconstruct(ssa_info, 1:2)
r_summed = sum(r, dims=1)[1, :, :, :]

h5write("data/eig_vals.h5", "eig_vals", ssa_info.eig_vals)
h5write("data/eig_vecs.h5", "eig_vecs", ssa_info.eig_vecs)
h5write("data/X.h5", "X", ssa_info.X)
h5write("data/C.h5", "C", ssa_info.C)
h5write("data/r.h5", "r", r)
h5write("data/r_summed.h5", "r_summed", r_summed)

x_ssa_fcst = x[:, :, n_years+1:end]
ssa_info = SSA.ssa_decompose(x_ssa_fcst, M)

ssa_info.eig_vals = eig_vals
ssa_info.eig_vecs = eig_vecs

r = SSA.ssa_reconstruct(ssa_info, 1:2)
r_summed = sum(r, dims=1)[1, :, :, :]

h5write("data/r_fcst.h5", "r", r)
h5write("data/r_summed_fcst.h5", "r_summed", r_summed)
