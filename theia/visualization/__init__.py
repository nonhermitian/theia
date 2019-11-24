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

"""
===========================================
Visualizations (:mod:`theia.visualization`)
===========================================

.. currentmodule:: theia.visualization

Functions
=========

.. autosummary::
   :toctree: ../stubs/

   iplot_histogram
   iplot_error_map
   job_summary
"""
from .counts_visualization import iplot_histogram
from .error_map import iplot_error_map
from .jobs import job_summary
