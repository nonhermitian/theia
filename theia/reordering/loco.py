# -*- coding: utf-8 -*-

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
# pylint: disable=invalid-name

"""Local ordering"""
import numpy as np
import scipy.sparse as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import cm
from ..cython.loco import (sparse_bandwidth, weighted_profile,
                           reverse_cuthill_mckee,
                           weighted_reverse_cuthill_mckee)
from ..cython.permute import sparse_permute
from ..visualization.spy import wspy


def local_ordering(circuit, weighted=True, verbose=False):
    """Permute qubit labels so that two-qubit gates are
    as local as possible.

    Parameters:
        circuit (qiskit.QuantumCircuit): An input quantum circuit.
        weighted (bool): Using weighting method.
        verbose (bool): Print values and plot results.

    Returns:
        tuple: permutation, bandwidth_reduction, profile_reduction

    Raises:
        ValueError: Circuit must have no >2Q gates and only a
                    single register.
    """
    rows = []
    cols = []
    data = []
    num_qubits = circuit.n_qubits
    num_regs = len(circuit.qregs)
    if num_regs != 1:
        raise ValueError('Circuit must have a single register.')

    for item in circuit.data:
        if item[0].name not in ['barrier', 'measure', 'snapshot']:
            nargs = len(item[1])
            if nargs == 2:
                rows.append(item[1][0].index)
                cols.append(item[1][1].index)
                data.append(1)
            elif nargs > 2:
                raise ValueError('Entangling gates must be 2Q gates only.')

    circ_graph = sp.coo_matrix((data, (rows, cols)), dtype=np.int32,
                               shape=(num_qubits, num_qubits)).tocsr()
    G = circ_graph + circ_graph.T

    _, _, ub = sparse_bandwidth(G.indices, G.indptr, G.shape[0])
    pro = weighted_profile(G.data, G.indices, G.indptr, G.shape[0])

    if verbose:
        fig, axes = plt.subplots(1, 2, figsize=(9, 4))
        wspy(G, ax=axes[0])
        print('Orig. bandwidth:', ub)
        print('Orig. weighted profile:', pro)

    if weighted:
        perm = weighted_reverse_cuthill_mckee(G.data, G.indices, G.indptr, G.shape[0])
    else:
        perm = reverse_cuthill_mckee(G.indices, G.indptr, G.shape[0])

    new_data, new_ind, new_ptr = sparse_permute(G.data,
                                                G.indices,
                                                G.indptr,
                                                G.shape[0],
                                                G.shape[1],
                                                perm, perm, 0)

    _, _, new_ub = sparse_bandwidth(new_ind, new_ptr, G.shape[0])
    F = sp.csr_matrix((new_data, new_ind, new_ptr), shape=G.shape)
    new_pro = weighted_profile(F.data, F.indices, F.indptr, F.shape[0])

    band_reduction = np.round((ub-new_ub)/ub*100, 2)
    pro_reduction = np.round((pro-new_pro)/pro*100, 2)
    if verbose:
        wspy(F, ax=axes[1], return_plot=False)
        cbaxes = fig.add_axes([0.95, 0.15, 0.02, 0.7])
        cmap = cm.magma
        norm = mpl.colors.Normalize(1, np.max(F.data.real))
        scmap = cm.ScalarMappable(norm=norm, cmap=cmap)
        cb = plt.colorbar(scmap, cax=cbaxes)
        _data_len = np.unique(F.data.real).shape[0]
        if _data_len > 11:
            _data_len = 11
        tick_locator = ticker.MaxNLocator(nbins=_data_len+1)
        cb.locator = tick_locator
        cb.update_ticks()
        axes[0].set_title("Input entangling graph", fontsize=16)
        axes[1].set_title("Permuted entangling graph", fontsize=16)
        print('New bandwidth:', new_ub)
        print('Bandwidth reduction', band_reduction, '%')
        print('New weighted profile:', new_pro)
        print('Profile reduction', pro_reduction, '%')
        plt.show(fig)

    return perm, band_reduction, pro_reduction
