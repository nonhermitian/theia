# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# pylint: disable=invalid-name

"""Weighted sparse matrix plot.
"""

import matplotlib as mpl
import numpy as np
from matplotlib import cm
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

def wspy(M, ax=None, fig_size=(5, 5), return_plot=True):
    """A weighted sparse matrix plotter.

    Parameters:
        M (csr_matrix): Input sparse matrix.
        ax (Matplotlib.Axes): Optional axes instance.
        fig_size (tuple): Figure size in inches.
        return_plot (bool): Return the plot axes instance.

    Returns:
        Axes: Plot axes instance if return_plot=True.
    """
    new_ax = False
    if ax is None:
        new_ax = True
        fig, ax = plt.subplots(1, 1, figsize=fig_size)
    cmap = cm.magma
    norm = mpl.colors.Normalize(1, np.max(M.data.real))
    nrows = M.shape[0]
    ptr = M.indptr
    ind = M.indices
    data = M.data
    for ii in range(nrows):
        for jj in range(ptr[ii], ptr[ii + 1]):
            ax.add_artist(Rectangle(xy=(ii-0.5, ind[jj]-0.5),
                                    width=1,
                                    height=1,
                                    color=cmap(norm(data[jj]))
                                    )
                         )
    ax.set_xlim(-0.5, M.shape[1]-0.5)
    ax.set_ylim(-0.5, M.shape[0]-0.5)
    ax.invert_yaxis()
    ax.set_aspect(float(M.shape[0])/float(M.shape[1]))
    ax.set_facecolor('#f6f6f6')
    ax.xaxis.tick_top()
    if new_ax:
        cbaxes = fig.add_axes([1, 0.15, 0.05, 0.7])
        plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbaxes)
    if return_plot:
        return ax
