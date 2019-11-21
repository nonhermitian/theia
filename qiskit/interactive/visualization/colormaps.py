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
import numpy as np
import seaborn as sns

HELIX_LIGHT = _sns_to_plotly(sns.cubehelix_palette(reverse=True, as_cmap=True))
HELIX_DARK = _sns_to_plotly(sns.cubehelix_palette(dark=0.25, light=0.97,
                                                  reverse=True, as_cmap=True))

def _sns_to_plotly(cmap, pl_entries=255):
    h = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])

    return pl_colorscale
