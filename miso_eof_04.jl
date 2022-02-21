using LinearAlgebra
using Statistics

using HDF5

D = 4964
N = 31625
n_pcs = 2

r = h5read("r_summed.h5", "r_summed")
r = permutedims(r, [2, 1, 3])
r = reshape(r, D, :)'

C = r'*r/N
u, s, v = svd(C)
pcs = r*v[:, 1:n_pcs]
std_pcs = std(pcs, dims=1)
pcs = pcs ./ std_pcs
eofs = v[:, 1:n_pcs] ./ std_pcs

h5write("eofs.h5", "eofs", eofs)
h5write("pcs.h5", "pcs", pcs)