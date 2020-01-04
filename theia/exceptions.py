# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Module for custom exceptions"""
import sys
from io import StringIO

class SilentExit(SystemExit):
    """A silent exception for Jupyter notebooks
    """
    def __init__(self):  #pylint: disable=super-init-not-called
        sys.stderr = StringIO()
        self.__class__.__name__ = ''

    def __del__(self):
        sys.stderr.flush()
        sys.stderr = sys.__stderr__
