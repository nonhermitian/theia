# -*- coding: utf-8 -*-
#cython: language_level = 3
#distutils: language = c++

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Functions for getting version information about ignis."""

import numpy as np
cimport numpy as cnp
cimport cython
cnp.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
def sparse_permute(
        cnp.ndarray[cython.numeric, ndim=1] data,
        int[::1] idx,
        int[::1] ptr,
        int nrows,
        int ncols,
        cnp.ndarray[int, ndim=1] rperm,
        cnp.ndarray[int, ndim=1] cperm,
        int flag):
    """
    Permutes the rows and columns of a sparse CSR or CSC matrix according to
    the permutation arrays rperm and cperm, respectively.
    Here, the permutation arrays specify the new order of the rows and columns.
    i.e. [0,1,2,3,4] -> [3,0,4,1,2].
    """
    cdef size_t ii, jj, kk, k0, nnz
    cdef cnp.ndarray[cython.numeric] new_data = np.zeros_like(data)
    cdef cnp.ndarray[int] new_idx = np.zeros_like(idx)
    cdef cnp.ndarray[int] new_ptr = np.zeros_like(ptr)
    cdef cnp.ndarray[int] perm_r
    cdef cnp.ndarray[int] perm_c
    cdef cnp.ndarray[int] inds

    if flag == 0:  # CSR matrix
        if rperm.shape[0] != 0:
            inds = np.argsort(rperm).astype(np.int32)
            perm_r = np.arange(rperm.shape[0], dtype=np.int32)[inds]

            for jj in range(nrows):
                ii = perm_r[jj]
                new_ptr[ii + 1] = ptr[jj + 1] - ptr[jj]

            for jj in range(nrows):
                new_ptr[jj + 1] = new_ptr[jj+1] + new_ptr[jj]

            for jj in range(nrows):
                k0 = new_ptr[perm_r[jj]]
                for kk in range(ptr[jj], ptr[jj + 1]):
                    new_idx[k0] = idx[kk]
                    new_data[k0] = data[kk]
                    k0 = k0 + 1

        if cperm.shape[0] != 0:
            inds = np.argsort(cperm).astype(np.int32)
            perm_c = np.arange(cperm.shape[0], dtype=np.int32)[inds]
            nnz = new_ptr[new_ptr.shape[0] - 1]
            for jj in range(nnz):
                new_idx[jj] = perm_c[new_idx[jj]]

    elif flag == 1:  # CSC matrix
        if cperm.shape[0] != 0:
            inds = np.argsort(cperm).astype(np.int32)
            perm_c = np.arange(cperm.shape[0], dtype=np.int32)[inds]

            for jj in range(ncols):
                ii = perm_c[jj]
                new_ptr[ii + 1] = ptr[jj + 1] - ptr[jj]

            for jj in range(ncols):
                new_ptr[jj + 1] = new_ptr[jj + 1] + new_ptr[jj]

            for jj in range(ncols):
                k0 = new_ptr[perm_c[jj]]
                for kk in range(ptr[jj], ptr[jj + 1]):
                    new_idx[k0] = idx[kk]
                    new_data[k0] = data[kk]
                    k0 = k0 + 1

        if rperm.shape[0] != 0:
            inds = np.argsort(rperm).astype(np.int32)
            perm_r = np.arange(rperm.shape[0], dtype=np.int32)[inds]
            nnz = new_ptr[new_ptr.shape[0] - 1]
            for jj in range(nnz):
                new_idx[jj] = perm_r[new_idx[jj]]

    return new_data, new_idx, new_ptr
