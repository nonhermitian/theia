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

import numpy as np
cimport numpy as cnp
cimport cython
from libc.stdint cimport int64_t
from libcpp.algorithm cimport sort
from libcpp.vector cimport vector
cnp.import_array()

cdef extern from "numpy/arrayobject.h" nogil:
    void PyArray_ENABLEFLAGS(cnp.ndarray arr, int flags)
    void PyDataMem_FREE(void * ptr)
    void PyDataMem_RENEW(void * ptr, size_t size)
    void PyDataMem_NEW_ZEROED(size_t size, size_t elsize)
    void PyDataMem_NEW(size_t size)

#Struct used for arg sorting
cdef struct _int_pair:
    int data
    int idx

#Struct used for weighted arg sorting
cdef struct _weighted_int_pair:
    int data
    int idx
    int weight

ctypedef _int_pair int_pair
ctypedef _weighted_int_pair weighted_int_pair
ctypedef int (*cfptr)(int_pair, int_pair)
ctypedef int (*wptr)(weighted_int_pair, weighted_int_pair)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int int_sort(int_pair x, int_pair y):
    return x.data < y.data

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int weighted_int_low_sort(weighted_int_pair x, 
                           weighted_int_pair y):
    if x.data != y.data:
        return x.data < y.data
    elif x.weight != y.weight:
        return x.weight < y.weight
    else:
        return 0
    
@cython.boundscheck(False)
@cython.wraparound(False)
cdef int weighted_int_high_sort(weighted_int_pair x, 
                           weighted_int_pair y):
    if x.data != y.data:
        return x.data < y.data
    elif x.weight != y.weight:
        return x.weight > y.weight
    else:
        return 0


@cython.boundscheck(False)
@cython.wraparound(False)
cdef int * _max_row_weights(
        int * data,
        int * inds,
        int * ptrs,
        int ncols):
    """
    Finds the largest abs value in each matrix column
    and the max. total number of elements in the cols (given by weights[-1]).

    Here we assume that the user already took the ABS value of the data.
    This keeps us from having to call abs over and over.

    """
    cdef int * weights = <int *>PyDataMem_NEW((ncols+1)*sizeof(int))
    cdef int ln, mx, ii, jj
    cdef int weight, current
    mx = 0
    for jj in range(ncols):
        ln = (ptrs[jj + 1] - ptrs[jj])
        if ln > mx:
            mx = ln

        weight = data[ptrs[jj]]
        for ii in range(ptrs[jj] + 1, ptrs[jj + 1]):
            current = data[ii]
            if current > weight:
                weight = current

        weights[jj] = weight

    weights[ncols] = mx
    return weights
    
    
@cython.boundscheck(False)
@cython.wraparound(False)
cdef int * int_argsort(int * x, int nrows):
    cdef vector[int_pair] pairs
    cdef cfptr cfptr_ = &int_sort
    cdef size_t kk
    pairs.resize(nrows)
    for kk in range(nrows):
        pairs[kk].data = x[kk]
        pairs[kk].idx = kk
    
    sort(pairs.begin(),pairs.end(),cfptr_)
    cdef int * out = <int *>PyDataMem_NEW(nrows *sizeof(int))
    for kk in range(nrows):
        out[kk] = pairs[kk].idx
    return out


@cython.boundscheck(False)
@cython.wraparound(False)
cdef int * weighted_int_argsort(int * data, 
                                int * inds,
                                int * ptr,
                                int * x, int nrows):
    cdef vector[weighted_int_pair] pairs
    cdef wptr wptr_ = &weighted_int_low_sort
    cdef size_t kk
    
    cdef int * weights = _max_row_weights(data,
                                              inds,
                                              ptr,
                                            nrows)
    pairs.resize(nrows)
    for kk in range(nrows):
        pairs[kk].data = x[kk]
        pairs[kk].idx = kk
        pairs[kk].weight = weights[kk]
    
    sort(pairs.begin(),pairs.end(),wptr_)
    cdef int * out = <int *>PyDataMem_NEW(nrows *sizeof(int))
    for kk in range(nrows):
        out[kk] = pairs[kk].idx
    PyDataMem_FREE(weights)
    return out



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef int[::1] _node_degrees(int[::1] ind, int[::1] ptr,
        unsigned int num_rows):

    cdef size_t ii, jj
    cdef int[::1] degree = np.zeros(num_rows, dtype=np.int32)

    for ii in range(num_rows):
        degree[ii] = ptr[ii + 1] - ptr[ii]
        for jj in range(ptr[ii], ptr[ii + 1]):
            if ind[jj] == ii:
                # add one if the diagonal is in row ii
                degree[ii] += 1
                break

    return degree



cdef inline int int_max(int x, int y):
    return x ^ ((x ^ y) & -(x < y))

@cython.boundscheck(False)
@cython.wraparound(False)
def sparse_bandwidth(
        int[::1] idx,
        int[::1] ptr,
        int nrows):
    """
    Calculates the max (mb), lower(lb), and upper(ub) bandwidths of a
    csr_matrix.
    """
    cdef int ldist
    cdef int lb = -nrows
    cdef int ub = -nrows
    cdef int mb = 0
    cdef size_t ii, jj

    for ii in range(nrows):
        for jj in range(ptr[ii], ptr[ii + 1]):
            ldist = ii - idx[jj]
            lb = int_max(lb, ldist)
            ub = int_max(ub, -ldist)
            mb = int_max(mb, ub + lb + 1)

    return mb, lb, ub


@cython.boundscheck(False)
@cython.wraparound(False)
def weighted_profile(int[::1] data,
                    int[::1] idx,
                    int[::1] ptr,
                    int nrows):
    cdef size_t ii, jj, 
    cdef int temp
    cdef int weighted_dist = 0
    cdef int64_t pro = 0
    for ii in range(nrows):
        temp = 0
        for jj in range(ptr[ii], ptr[ii + 1]):
            if idx[jj] >= ii:
                weighted_dist = (idx[jj] - ii)*data[jj]
            else:
                weighted_dist = (ii - idx[jj])*data[jj]
            temp = int_max(temp, weighted_dist)
        pro += temp
    return pro


@cython.boundscheck(False)
@cython.wraparound(False)
def reverse_cuthill_mckee(int[::1] ind, int[::1] ptr, int num_rows):
    """
    Reverse Cuthill-McKee ordering of a sparse csr or csc matrix.
    """
    cdef unsigned int N = 0, N_old, seed, level_start, level_end
    cdef unsigned int zz, i, j, ii, jj, kk, ll, level_len, temp, temp2
    cdef cnp.ndarray[int, ndim=1] order = np.zeros(num_rows, dtype=np.int32)
    cdef int[::1] degree = _node_degrees(ind, ptr, num_rows)
    cdef int * inds = int_argsort(&degree[0], num_rows)
    cdef int * rev_inds = int_argsort(inds, num_rows)
    cdef int * temp_degrees = NULL
    
    cdef cfptr cfptr_ = &int_sort
    cdef vector[int_pair] pairs

    # loop over zz takes into account possible disconnected graph.
    for zz in range(num_rows):
        if inds[zz] != -1:   # Do BFS with seed=inds[zz]
            seed = inds[zz]
            order[N] = seed
            N += 1
            inds[rev_inds[seed]] = -1
            level_start = N - 1
            level_end = N

            while level_start < level_end:
                for ii in range(level_start, level_end):
                    i = order[ii]
                    N_old = N

                    # add unvisited neighbors
                    for jj in range(ptr[i], ptr[i + 1]):
                        # j is node number connected to i
                        j = ind[jj]
                        if inds[rev_inds[j]] != -1:
                            inds[rev_inds[j]] = -1
                            order[N] = j
                            N += 1
                    
                    # Do the low -> high sorting here
                    pairs.resize((N-N_old))
                    level_len = 0
                    for kk in range(N_old, N):
                        pairs[level_len].data = degree[order[kk]]
                        pairs[level_len].idx = order[N_old+level_len]
                        level_len += 1
                    
                    sort(pairs.begin(),pairs.end(),cfptr_)
                    
                    for kk in range(level_len):
                        order[N_old+kk] = pairs[kk].idx

                # set next level start and end ranges
                level_start = level_end
                level_end = N

        if N == num_rows:
            break
    PyDataMem_FREE(inds)
    PyDataMem_FREE(rev_inds)
    PyDataMem_FREE(temp_degrees)
    # return reversed order for RCM ordering
    return order[::-1]


@cython.boundscheck(False)
@cython.wraparound(False)
def weighted_reverse_cuthill_mckee(int[::1] data, 
                                   int[::1] ind, 
                                   int[::1] ptr, 
                                   int num_rows):
    """
    Reverse Cuthill-McKee ordering of a sparse csr or csc matrix.
    """
    cdef unsigned int N = 0, N_old, seed, level_start, level_end
    cdef unsigned int zz, i, j, ii, jj, kk, ll, level_len, temp, temp2
    cdef cnp.ndarray[int, ndim=1] order = np.zeros(num_rows, dtype=np.int32)
    cdef int[::1] degree = _node_degrees(ind, ptr, num_rows)
    cdef int * inds = weighted_int_argsort(&data[0],
                                           &ind[0],
                                           &ptr[0],
                                           &degree[0], num_rows)
    cdef int * rev_inds = int_argsort(inds, num_rows)
    
    cdef wptr wptr_ = &weighted_int_high_sort
    cdef vector[weighted_int_pair] pairs

    # loop over zz takes into account possible disconnected graph.
    for zz in range(num_rows):
        if inds[zz] != -1:   # Do BFS with seed=inds[zz]
            seed = inds[zz]
            order[N] = seed
            N += 1
            inds[rev_inds[seed]] = -1
            level_start = N - 1
            level_end = N

            while level_start < level_end:
                for ii in range(level_start, level_end):
                    i = order[ii]
                    N_old = N

                    # add unvisited neighbors
                    for jj in range(ptr[i], ptr[i + 1]):
                        # j is node number connected to i
                        j = ind[jj]
                        if inds[rev_inds[j]] != -1:
                            inds[rev_inds[j]] = -1
                            order[N] = j
                            N += 1

                    # Do the low -> high sorting here
                    pairs.resize((N-N_old))
                    level_len = 0
                    for kk in range(N_old, N):
                        pairs[level_len].data = degree[order[kk]]
                        pairs[level_len].idx = order[N_old+level_len]
                        pairs[level_len].weight = data[order[kk]]
                        level_len += 1
                    
                    sort(pairs.begin(),pairs.end(),wptr_)
                    for kk in range(level_len):
                        order[N_old+kk] = pairs[kk].idx

                # set next level start and end ranges
                level_start = level_end
                level_end = N

        if N == num_rows:
            break
    PyDataMem_FREE(inds)
    PyDataMem_FREE(rev_inds)
    # return reversed order for RCM ordering
    return order[::-1]
